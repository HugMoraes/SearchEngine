from src.insertDocs.utils import SearchFieldsConfig

class QueryConfig:
    # A lógica de setup das técnicas válidas permanece a mesma
    combined_techniques = SearchFieldsConfig.COMMON_TECHNIQUES + SearchFieldsConfig.EXCLUSIVE_OPTIONAL_TECHNIQUES
    flattened_techniques = (
        tech for item in combined_techniques for tech in (item if isinstance(item, list) else [item])
    )
    ALL_VALID_TECHNIQUES = set(flattened_techniques)

    def __init__(self, text_techniques_list: list[str] = None, ai_text: bool = False, ai_global_expansion: bool = False):
        """
        Inicializa a configuração da consulta.

        Args:
            text_techniques_list (list[str], optional): Uma lista com os nomes das
                técnicas de texto a serem aplicadas. Ex: ['remove_stopwords', 'stemming'].
                Defaults to None.
            ai_text (bool, optional): Flag para habilitar IA na busca de texto. Defaults to False.
            ai_global_expansion (bool, optional): Flag para habilitar expansão global
                de IA. Defaults to False.

        Raises:
            ValueError: Se uma combinação inválida de técnicas for fornecida ou
                        se uma técnica desconhecida for passada.
        """
        self.text_techniques = []
        self.fields = []
        self.ai_text = ai_text
        self.ai_global_expansion = ai_global_expansion

        # --- LÓGICA DE GERAÇÃO DE CAMPOS ATUALIZADA ---

        # CASO 1: Existem técnicas de texto a serem aplicadas.
        if text_techniques_list:
            self._validate_and_generate_fields(text_techniques_list)
        # CASO 2: Nenhuma técnica de texto é fornecida. Usa os campos padrão.
        else:
            self.fields = ['document.body', 'document.title', 'document.highlight']

        # REGRA ADICIONAL: Adiciona o campo de busca por IA se a flag estiver ativa.
        # Isso é executado independentemente de haver técnicas de texto ou não.
        if self.ai_text:
            self.fields.append('search_fields.ai_text')

    def _validate_and_generate_fields(self, techniques: list[str]):
        """
        Valida a lista de técnicas e gera os nomes dos campos para a busca.
        (Este método permanece inalterado)
        """
        input_techniques = set(techniques)

        # 1. Validação: Técnica desconhecida
        unknown_techniques = input_techniques - self.ALL_VALID_TECHNIQUES
        if unknown_techniques:
            raise ValueError(f"Técnica(s) de texto desconhecida(s): {', '.join(unknown_techniques)}")

        # 2. Validação: Técnicas exclusivas
        exclusive_flat = {
            tech for item in SearchFieldsConfig.EXCLUSIVE_OPTIONAL_TECHNIQUES 
            for tech in (item if isinstance(item, list) else [item])
        }
        
        exclusive_techniques_found = input_techniques.intersection(exclusive_flat)
        
        if len(exclusive_techniques_found) > 1:
            raise ValueError(
                "Combinação de técnicas inválida. As seguintes técnicas são mutuamente exclusivas "
                f"e apenas uma pode ser usada por vez: {', '.join(exclusive_techniques_found)}"
            )

        self.text_techniques = sorted(list(input_techniques))
        
        # Cria um único sufixo a partir das técnicas ordenadas.
        techniques_suffix = "_".join(self.text_techniques)

        # Gera um campo de busca para cada campo base anexando o sufixo combinado.
        generated_fields = []
        for field_name in sorted(SearchFieldsConfig.FIELDS):
            generated_fields.append(f"search_fields.{field_name}_{techniques_suffix}")
        
        self.fields = generated_fields

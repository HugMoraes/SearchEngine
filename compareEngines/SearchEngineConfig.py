import yaml
from typing import Any, Dict, Optional, List
from compareEngines.allowed_options import ALLOWED_OPTIONS

class SearchEngineConfig:
    """
    Uma classe para carregar, validar e fornecer acesso às configurações
    de um motor de busca a partir de um arquivo YAML.
    A validação é executada automaticamente na inicialização.
    """

    def __init__(self, config_path: str):
        """
        Inicializa o objeto, carregando e validando o arquivo YAML.

        Args:
            config_path (str): O caminho para o arquivo de configuração YAML.

        Raises:
            ValueError: Se a configuração for inválida.
            FileNotFoundError: Se o arquivo não for encontrado.
            yaml.YAMLError: Se o arquivo tiver sintaxe YAML inválida.
        """
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self.errors: List[str] = []
        
        # Carrega a configuração
        self._config = self._load_config()
        
        # Valida a configuração carregada
        if not self._validate():
            error_summary = "\n❌ A configuração é inválida. Erros encontrados:\n"
            for error in self.errors:
                error_summary += f"   - {error}\n"
            raise ValueError(error_summary)
        
        print("✅ Configuração validada com sucesso.")

    def _load_config(self) -> Dict[str, Any]:
        """Carrega o arquivo YAML e o converte em um dicionário Python."""
        print(f"🔄 Carregando configuração de '{self.config_path}'...")
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                if not isinstance(config_data, dict):
                    raise yaml.YAMLError("O conteúdo do YAML deve ser um dicionário (objeto).")
                print("👍 Arquivo YAML carregado.")
                return config_data
        except FileNotFoundError:
            print(f"❌ Erro Crítico: O arquivo de configuração '{self.config_path}' não foi encontrado.")
            raise
        except yaml.YAMLError as e:
            print(f"❌ Erro Crítico: O arquivo YAML '{self.config_path}' contém um erro de sintaxe: {e}")
            raise
        return {}

    def _add_error(self, message: str):
        """Adiciona uma mensagem de erro à lista."""
        self.errors.append(message)

    def _validate(self) -> bool:
        """Executa todas as verificações de validação. Interno."""
        self.errors = []
        self._validate_query_expansion()
        self._validate_search_fields()
        return not self.errors

    def _validate_query_expansion(self):
        """Valida a seção 'query-expansion'."""
        qe_config = self.query_expansion
        if not qe_config: return

        # Valida a estratégia global
        global_strategy = qe_config.get('global-expansion-strategy')
        # CORREÇÃO: Trata 'None' como um valor válido (desativado) e só valida se não for None.
        if global_strategy and global_strategy not in ALLOWED_OPTIONS["global-expansion-strategy"]:
            self._add_error(f"[query-expansion] Estratégia global inválida: '{global_strategy}'.")

        # Valida a estratégia local
        local_strategy = qe_config.get('local-expansion-strategy')
        # CORREÇÃO: Mesma lógica para a estratégia local.
        if local_strategy and local_strategy not in ALLOWED_OPTIONS["local-expansion-strategy"]:
            self._add_error(f"[query-expansion] Estratégia local inválida: '{local_strategy}'.")

    def _validate_search_fields(self):
        """Inicia a validação recursiva da seção 'search-fields'."""
        fields_config = self.search_fields
        if fields_config and isinstance(fields_config, dict):
            self._validate_field_recursive(fields_config, [])
        elif fields_config:
            self._add_error("'search-fields' deve ser um dicionário.")

    def _validate_field_recursive(self, current_level: Dict[str, Any], path: List[str]):
        """Navega e valida os campos recursivamente."""
        for key, value in current_level.items():
            current_path = path + [key]
            if isinstance(value, dict):
                if 'transformations' in value or 'weight' in value:
                    self._validate_field_properties(value, current_path)
                else:
                    self._validate_field_recursive(value, current_path)

    def _validate_field_properties(self, props: Dict[str, Any], path: List[str]):
        """Valida 'transformations' e 'weight' de um campo."""
        path_str = ".".join(path)
        if 'transformations' in props:
            trans = props['transformations']
            if not isinstance(trans, list):
                self._add_error(f"'{path_str}.transformations' deve ser uma lista.")
            else:
                for t in trans:
                    if t not in ALLOWED_OPTIONS["transformations"]:
                        self._add_error(f"'{path_str}' possui uma transformação inválida: '{t}'.")
        
        if 'weight' in props:
            if not isinstance(props['weight'], (int, float)):
                self._add_error(f"'{path_str}.weight' deve ser um número (int ou float).")

    @property
    def query_expansion(self) -> Optional[Dict[str, Any]]:
        """Retorna a seção de configuração de expansão de consulta."""
        return self._config.get('query-expansion')

    @property
    def search_fields(self) -> Optional[Dict[str, Any]]:
        """Retorna a seção de configuração dos campos de busca."""
        return self._config.get('search-fields')

    def get_field_config(self, field_name: str) -> Optional[Dict[str, Any]]:
        """Obtém a configuração para um campo específico (ex: 'document.title')."""
        if not self.search_fields: return None
        keys, current_level = field_name.split('.'), self.search_fields
        for key in keys:
            current_level = current_level.get(key)
            if current_level is None: return None
        return current_level

    def display_full_config(self):
        """
        Imprime uma visualização completa e organizada da configuração carregada.
        """
        print("\n" + "="*50)
        print("           RESUMO COMPLETO DA CONFIGURAÇÃO")
        print("="*50)
        print(f"Arquivo de Origem: '{self.config_path}'\n")

        # Exibe Query Expansion
        if self.query_expansion:
            print("▶️  Expansão de Consulta:")
            for key, value in self.query_expansion.items():
                print(f"   - {key}: {value if value is not None else 'desativado'}")
        else:
            print("▶️  Expansão de Consulta: desativado")

        # Exibe Search Fields
        print("\n▶️  Campos de Busca:")
        if self.search_fields:
            self._display_field_recursive(self.search_fields, 1)
        else:
            print("   Nenhum campo de busca configurado.")
        
        print("\n" + "="*50)

    def _display_field_recursive(self, current_level: Dict, indent_level: int):
        """Função auxiliar para imprimir os campos de forma aninhada."""
        indent = "  " * indent_level
        for key, value in current_level.items():
            if isinstance(value, dict) and ('transformations' in value or 'weight' in value):
                print(f"{indent}↳ [Campo] {key}:")
                if 'weight' in value:
                    print(f"{indent}  - Peso: {value['weight']}")
                if 'transformations' in value:
                    print(f"{indent}  - Transformações: {value['transformations']}")
            elif isinstance(value, dict):
                print(f"{indent}📁 {key}:")
                self._display_field_recursive(value, indent_level + 1)

    def __repr__(self) -> str:
        return f"SearchEngineConfig(path='{self.config_path}', valid={not self.errors})"


# ================== TESTE 1: CONFIGURAÇÃO VÁLIDA ==================
print("\n--- TESTE 1: TENTANDO CARREGAR UMA CONFIGURAÇÃO VÁLIDA ---")
# CORREÇÃO: A indentação do YAML foi ajustada para ser válida.
valid_config_content = """
query-expansion:
  global-expansion-strategy: thesaurus
  local-expansion-strategy: null
search-fields:
  document:
    title:
      transformations: [case-normalization, ascii-folding, remove-stopwords]
      weight: 3
    body:
      transformations: [lematization, remove-stopwords]
      weight: 1
  metadata:
    tags:
      transformations: [case-normalization]
      weight: 5
"""
with open('config_valida.yml', 'w', encoding='utf-8') as f:
    f.write(valid_config_content)

try:
    config_ok = SearchEngineConfig('config_valida.yml')
    config_ok.display_full_config()
except (ValueError, FileNotFoundError, yaml.YAMLError) as e:
    print(e)

# ================== TESTE 2: CONFIGURAÇÃO INVÁLIDA ==================
print("\n\n--- TESTE 2: TENTANDO CARREGAR UMA CONFIGURAÇÃO INVÁLIDA ---")
# CORREÇÃO: A indentação do YAML foi ajustada para que os erros possam ser encontrados.
invalid_config_content = """
query-expansion:
  global-expansion-strategy: word2vec # Inválido
  local-expansion-strategy: null
search-fields:
  document:
    title:
      transformations: [case-normalization, ascii-folding] # Erro de digitação
      weight: "alta" # Tipo inválido
"""
with open('config_invalida.yml', 'w', encoding='utf-8') as f:
    f.write(invalid_config_content)

try:
    config_nok = SearchEngineConfig('config_invalida.yml')
except ValueError as e:
    print(e)
except (FileNotFoundError, yaml.YAMLError) as e:
    print(f"Erro inesperado durante o teste: {e}")

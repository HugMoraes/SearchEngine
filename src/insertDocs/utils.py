from src.insertDocs.SearchFieldsModels import SearchFieldsConfig, SearchField
from itertools import chain, combinations as iter_combinations, product

def generate_search_field_combinations(config: SearchFieldsConfig) -> list[SearchField]:
    """
    Gera TODAS as combinações possíveis de técnicas para cada campo,
    garantindo que cada combinação tenha pelo menos uma técnica.

    A função trata tanto as técnicas comuns quanto as exclusivas como opcionais,
    mas respeita as regras de exclusividade.

    Args:
        config: Uma instância da classe de configuração SearchFieldsConfig.

    Returns:
        Uma lista de instâncias de SearchField com todas as combinações válidas.
    """
    
    # 1. Gerar o "power set" (todos os subconjuntos) das técnicas comuns.
    # Isso nos dará combinações com zero, uma ou ambas as técnicas comuns.
    common_techs = config.COMMON_TECHNIQUES
    common_subsets = list(chain.from_iterable(iter_combinations(common_techs, r) for r in range(len(common_techs) + 1)))
    # Resultado: [(), ('remove_stopwords',), ('lowercase_text',), ('remove_stopwords', 'lowercase_text')]

    # 2. Gerar as escolhas possíveis para os grupos de técnicas exclusivas.
    # Adicionamos 'None' para representar a escolha de não usar nenhuma técnica do grupo.
    exclusive_groups_with_none = [group + [None] for group in config.EXCLUSIVE_OPTIONAL_TECHNIQUES]
    exclusive_choices = list(product(*exclusive_groups_with_none))
    # Resultado: [('steamming',), ('lematization',), (None,)]

    # 3. Combinar tudo e filtrar
    valid_technique_sets = set()

    for common_combo_tuple in common_subsets:
        for exclusive_choice_tuple in exclusive_choices:
            
            # Monta a lista de técnicas da combinação atual
            current_techniques = list(common_combo_tuple)
            current_techniques.extend([tech for tech in exclusive_choice_tuple if tech is not None])
            
            # 4. Garantir a regra de "pelo menos uma técnica"
            if len(current_techniques) > 0:
                # Adiciona a tupla ordenada a um set para garantir unicidade
                valid_technique_sets.add(tuple(sorted(current_techniques)))

    # 5. Criar as instâncias de SearchField para cada campo
    all_combinations = []
    for field in config.FIELDS:
        for tech_set_tuple in sorted(list(valid_technique_sets)): # Ordena para um resultado previsível
            all_combinations.append(SearchField(techniques=list(tech_set_tuple), from_field=field))
            
    return all_combinations

for i in generate_search_field_combinations(SearchFieldsConfig):
    print(i)
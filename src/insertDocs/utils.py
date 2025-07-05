from itertools import combinations, product

def gerar_combinacoes_generalizadas(opcionais_comuns: list, grupos_exclusivos: list[list]):
    """
    Gera todas as combinações válidas de itens, dadas as regras de exclusividade.

    Args:
        opcionais_comuns (list): Uma lista de itens que podem ser livremente combinados.
        grupos_exclusivos (list[list]): Uma lista de listas. Cada lista interna é um grupo
                                        de itens mutuamente exclusivos (apenas um pode ser
                                        escolhido por combinação).

    Returns:
        list[list]: Uma lista com todas as combinações válidas possíveis. A lista é
                    ordenada por tamanho e depois alfabeticamente para consistência.
    """
    
    # --- Passo 1: Gerar todas as combinações possíveis dos itens comuns ---
    # Isso inclui a combinação vazia (não escolher nenhum item comum).
    combos_comuns = []
    for r in range(len(opcionais_comuns) + 1):
        for combo in combinations(opcionais_comuns, r):
            combos_comuns.append(list(combo))

    # --- Passo 2: Gerar todas as escolhas válidas dos grupos exclusivos ---
    # Para cada grupo, adicionamos 'None' para representar a escolha de "nenhum item deste grupo".
    opcoes_dos_grupos = []
    for grupo in grupos_exclusivos:
        opcoes_dos_grupos.append(grupo + [None])
    
    # Usamos itertools.product para obter o produto cartesiano de todas as escolhas possíveis.
    # Cada resultado do product é uma tupla com uma escolha de cada grupo.
    # Ex: ('Stemming', 'BERT'), ('Stemming', None), ('Lematização', 'Word2Vec'), etc.
    combos_exclusivos_raw = product(*opcoes_dos_grupos)

    # Limpamos os resultados, removendo os 'None' para formar as combinações finais.
    combos_exclusivos = []
    for combo_tuple in combos_exclusivos_raw:
        # Filtra os 'None' e cria uma lista limpa
        clean_combo = [item for item in combo_tuple if item is not None]
        combos_exclusivos.append(clean_combo)

    # --- Passo 3: Combinar os resultados e remover duplicatas ---
    resultados_finais = set()
    for c_comum in combos_comuns:
        for c_exclusivo in combos_exclusivos:
            # Combina a parte comum com a parte exclusiva
            final_combo = tuple(sorted(c_comum + c_exclusivo))
            resultados_finais.add(final_combo)
            
    # Converte o set de tuplas de volta para uma lista de listas
    lista_de_resultados = [list(combo) for combo in resultados_finais]

    # Ordena a lista final para uma exibição mais clara (primeiro por tamanho, depois alfabeticamente)
    lista_de_resultados.sort(key=lambda x: (len(x), x))
    
    return lista_de_resultados

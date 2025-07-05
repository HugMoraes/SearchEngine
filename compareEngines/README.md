# Guia de Configuração de Busca Avançada

Este documento serve como uma referência completa para entender os conceitos e as opções disponíveis no arquivo `config.yml`, que gerencia o comportamento do nosso mecanismo de busca.

---

## 1. Expansão de Consulta (Query Expansion)

A **expansão de consulta** é o processo de reescrever a consulta original de um usuário para melhorar a qualidade dos resultados. O objetivo principal é diminuir a falha de correspondência de vocabulário (quando o usuário e o conteúdo usam termos diferentes para o mesmo conceito), adicionando termos relevantes como sinônimos, variações ou conceitos relacionados.

### 1.1. Expansões Locais (Análise de Feedback de Relevância)

Analisam os documentos mais bem classificados (top-K) da consulta **original** para extrair novos termos e refinar a busca. A premissa é que esses primeiros resultados são relevantes e contêm palavras-chave valiosas.

#### Opções de Escolha:
* **Análise de Feedback de Relevância Pseudo/Automático**: Assume que os 'N' primeiros documentos são relevantes e extrai os termos mais frequentes e distintivos deles para adicionar à consulta.
* **Análise de Cluster de Documentos**: Agrupa os documentos de topo em clusters temáticos e extrai os termos que melhor representam o centro de cada cluster.
* **Modelo de Relevância Rocchio**: Um método clássico que ajusta o vetor da consulta original usando os vetores dos documentos de topo considerados relevantes.

### 1.2. Expansões Globais (Análise de Coleção)

Utilizam fontes de conhecimento **externas** e independentes da consulta para encontrar termos relacionados. Esta expansão ocorre antes mesmo da consulta inicial ser executada na coleção de documentos.

#### Opções de Escolha:
* **Dicionário de Sinônimos (Thesaurus)**: Usa um dicionário pré-definido para adicionar sinônimos diretos à consulta (ex: "carro" -> "automóvel", "veículo").
* **WordNet / Redes Semânticas**: Utiliza uma base de dados lexical para encontrar relações semânticas mais complexas, como hiperônimos (termos mais gerais) e hipônimos (termos mais específicos).
* **Modelos de Linguagem (Word Embeddings)**: Usa modelos como Word2Vec, GloVe ou BERT para encontrar palavras que aparecem em contextos semelhantes, capturando relações semânticas e contextuais (ex: "inteligência artificial" -> "machine learning", "redes neurais").

---

## 2. Campos de Busca (Search Fields)

Define os campos específicos dos documentos (mapeados no Elasticsearch ou outro motor de busca) onde a busca será executada. Cada campo pode ter seu próprio peso e conjunto de transformações.

### 2.1. Transformações (Transformations)

São processos aplicados ao texto (tanto da consulta quanto dos campos) para normalizar e enriquecer os dados, aumentando a probabilidade de uma correspondência relevante.

#### Opções de Escolha:
* **`case-normalization`**: Converte todo o texto para minúsculas. Essencial para que "Casa" e "casa" sejam tratados como o mesmo termo.
* **`remove-punctuation` / `remove-special-characters`**: Elimina caracteres como `,`, `.`, `!`, `@`, etc.
* **`remove-stopwords`**: Remove palavras extremamente comuns que raramente contribuem para o significado (ex: "o", "a", "de", "que", "em").
* **`stemming` (Redução ao Radical)**: Reduz as palavras à sua raiz/radical, mesmo que o resultado não seja uma palavra real (ex: "programando", "programador" -> "program"). É mais rápido e agressivo.
* **`lematization` (Lematização)**: Reduz as palavras à sua forma dicionarizada fundamental (lema), resultando sempre em uma palavra válida (ex: "fui", "indo" -> "ir"). É mais lento, porém mais preciso.
* **`ascii-folding`**: Remove acentos e diacríticos das palavras (ex: "canção" -> "cancao"). Crucial para buscas em português.
* **`synonym-expansion`**: Aplica um arquivo de sinônimos para expandir termos.
* **`ai-expand-text`**: Utiliza modelos de IA para expandir o texto com conceitos e termos semanticamente relacionados.

### 2.2. Peso (Weight)

Um multiplicador numérico que aumenta ou diminui a pontuação de relevância de um campo. Um campo com `weight: 2` tem o dobro da importância de um campo com `weight: 1` na determinação do score final de um documento. Isso permite que uma correspondência no título seja mais significativa do que uma no corpo do texto.

---

## 3. Exemplos Práticos

### Exemplo 1: Busca em um E-commerce de Eletrônicos

Imagine que um usuário busca por **"fone sem fio pra jogo"**.

#### Configuração (`config.yml`):
```yaml
query-expansion:
  global-expansion-strategy: thesaurus

search-fields:
  document:
    title:
      transformations: [case-normalization, ascii-folding]
      weight: 3
    short_description:
      transformations: [case-normalization, ascii-folding, remove-stopwords]
      weight: 2
    full_description:
      transformations: [case-normalization, ascii-folding, remove-stopwords, stemming]
      weight: 1
```

#### Explicação do Processo:

1.  **Transformação da Consulta**: A consulta "fone sem fio pra jogo" passa pelas transformações básicas:
    * `case-normalization` & `ascii-folding` -> `"fone sem fio pra jogo"`
    * `remove-stopwords` -> `"fone fio jogo"` (assumindo que "sem" e "pra" são stopwords)

2.  **Expansão Global (Thesaurus)**: O sistema consulta o dicionário de sinônimos:
    * `fone` -> `(fone OR headset OR "fone de ouvido")`
    * `jogo` -> `(jogo OR gamer OR gaming)`
    * **Consulta Final Expandida**: `(fone OR headset OR "fone de ouvido") AND fio AND (jogo OR gamer OR gaming)`

3.  **Busca e Pontuação**: O sistema agora busca por essa consulta expandida nos campos.
    * Um produto com título **"Headset Gamer Redragon"** será encontrado, pois `Headset` e `Gamer` correspondem aos termos expandidos.
    * Como a correspondência ocorreu no campo `title` (`weight: 3`), este produto receberá uma pontuação de relevância alta.
    * Outro produto que mencione "fone de ouvido" na `full_description` (`weight: 1`) também será encontrado, mas provavelmente com uma pontuação menor.

### Exemplo 2: Busca em um Portal de Notícias

Um usuário busca por **"Impacto da Inteligência Artificial"**.

#### Configuração (`config.yml`):
```yaml
query-expansion: null

search-fields:
  document:
    title:
      transformations: [case-normalization, ascii-folding]
      weight: 2
    body:
      transformations: [case-normalization, ascii-folding, lematization, ai-expand-text]
      weight: 1
```

#### Explicação do Processo:

1.  **Transformação da Consulta**: A consulta é normalizada para `"impacto da inteligencia artificial"`.

2.  **Busca no Campo `body`**: O texto do campo `body` de uma notícia passa por várias transformações.
    * `lematization`: Palavras como "aprendendo", "aprendeu" viram "aprender".
    * `ai-expand-text`: Ao processar o texto "inteligência artificial", a IA pode enriquecê-lo com termos semanticamente próximos como "machine learning", "redes neurais", "processamento de linguagem natural", "IA generativa", etc.

3.  **Resultado**: Graças à expansão com IA no campo `body`, a busca do usuário por "Inteligência Artificial" encontrará uma notícia que talvez não use exatamente essas palavras, mas fale extensivamente sobre **"machine learning"** e **"redes neurais"**. Isso resulta em uma busca conceitual e muito mais poderosa, que vai além da simples correspondência de palavras-chave.
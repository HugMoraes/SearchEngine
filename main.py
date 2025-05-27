import pandas as pd

# Lê o arquivo parquet
df = pd.read_parquet('data/baseDocumentos')

# Exibe as primeiras linhas do DataFrame
print("\nPrimeiras linhas do arquivo:")
print(df.head())

# Exibe informações sobre o DataFrame
print("\nInformações sobre o DataFrame:")
print(df.info())

# Exibe estatísticas descritivas
print("\nEstatísticas descritivas:")
print(df.describe()) 

for index, row in df.iterrows():
        metaData = row['metadata'].keys()
        print("metadata\n",metaData)
        keys = row['document'].keys()
        print("document\n",keys)
        print(row['document']['body'])
        if index > 10:
            break

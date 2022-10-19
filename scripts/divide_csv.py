import pandas as pd

df = pd.read_csv('src/db/base.csv', sep=';')
df_states = df[(~df['estado'].isna()) & (~df['codmun'].isna())]
df_brasil = df[df.regiao == 'Brasil']
df_states.to_csv('src/db/states.csv')
df_brasil.to_csv('src/db/brasil.csv')

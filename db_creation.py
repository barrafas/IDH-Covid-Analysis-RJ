#====================#
#  Creating database #
#   04/11 - 16:38    #
#====================#
import pandas as pd
import geopandas as gpd
import sqlite3
import basedosdados as bd
from shapely import wkt

# Lendo arquivo (raw string - não é a melhor forma)
df = gpd.read_file(r'geojson\brasil.json')

# Removendo coluna de descrição
df = df.drop(['description'], axis=1)

# Transformando o objeto geometria em texto (para fazer o INSERT)
df['geometry'] = df['geometry'].apply(wkt.dumps)

# Pegando uma base de dados que conecta a sigla de um estado à cada município por seu ID
states = bd.read_sql(
    '''
    SELECT DISTINCT id_municipio AS id, sigla_uf
    FROM  basedosdados.br_bd_diretorios_brasil.setor_censitario AS censo
    GROUP BY id_municipio, sigla_uf
    ''',
    billing_project_id='geobr-analysis')

# Dando merge dos dois dataframes
df = pd.merge(states, df, on='id')

# Criando/conectando database
conn = sqlite3.connect('cities.db')

# Ativando o spatialite (old/cringe)
conn.enable_load_extension(True)
conn.load_extension('mod_spatialite.dll')

# Criando cursor e ativando spatialite
c = conn.cursor()
c.execute('SELECT load_extension("mod_spatialite.dll")')
c.execute('SELECT InitSpatialMetaData()')

# Criando tabela
c.execute('create table cities (id integer primary key, sigla_uf text, name text)')

# Criando coluna e index para geometria
c.execute("SELECT AddGeometryColumn('cities', 'geometry', 4326, 'POLYGON', 'XY');")
c.execute("SELECT CreateSpatialIndex('cities', 'geometry');")

# Commit
conn.commit()

# Importando df para o db
df.to_sql('cities', conn, if_exists='replace',index=False)

#Fechando conexão
c.close()
conn.close()
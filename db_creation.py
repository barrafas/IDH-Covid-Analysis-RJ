#====================#
#  Creating database #
#   04/11 - 16:38    #
#====================#
import pandas as pd
import geopandas as gpd
import sqlite3
import basedosdados as bd
from shapely import wkt, wkb

# Lendo arquivo (raw string - não é a melhor forma)
df = gpd.read_file(r'geojson\brasil.json')

# Removendo coluna de descrição
df = df.drop(['description'], axis=1)

# Pegando uma base de dados que conecta a sigla de um estado à cada município por seu ID
states = bd.read_sql(
    '''
    SELECT DISTINCT id_municipio AS id, sigla_uf
    FROM  basedosdados.br_bd_diretorios_brasil.setor_censitario AS censo
    GROUP BY id_municipio, sigla_uf
    ''',
    billing_project_id='adameplayground')

# Dando merge dos dois dataframes
df = pd.merge(states, df, on='id')

# Criando relação id - geometria
records = [(wkt.dumps(df.geometry.iloc[i]), df.id.iloc[i]) for i in range(df.shape[0])]

# Removendo coluna espacial
df = df.drop(['geometry'], axis=1)

# Criando/conectando database
conn = sqlite3.connect('cities.db')
c = conn.cursor()

# Criando tabela
c.execute('create table cities (id integer primary key, sigla_uf text, name text)')

# Importando dados não-geométricos para o db
df.to_sql('cities', conn, if_exists='replace',index=False)

# Ativando o spatialite
conn.enable_load_extension(True)
conn.load_extension('mod_spatialite.dll')

# Ativando spatialite
c.execute('SELECT load_extension("mod_spatialite.dll")')
c.execute('SELECT InitSpatialMetaData()')

# Criando coluna e index para geometria
c.execute("SELECT AddGeometryColumn('cities', 'geometry', 3857, 'polygon', 'XY');")

# Spatialite geometry objects
# c.execute("UPDATE cities SET geometry=CastToMultiPolygon(GeomFromText(geometry, -1));")
c.execute("SELECT CreateSpatialIndex('cities', 'geometry');")

conn.executemany(
        """
        UPDATE cities
        SET geometry=GeomFromText(?, 3857)
        WHERE id = ?
        """, records
    )

# Commit
conn.commit()



#Fechando conexão
c.close()
conn.close()
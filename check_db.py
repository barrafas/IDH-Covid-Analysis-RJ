#====================#
#  Checking database #
#   04/11 - 16:38    #
#====================#
import sqlite3

# Conectando database
conn = sqlite3.connect('cities.db')

# Ativando o spatialite (old/cringe)
conn.enable_load_extension(True)
conn.load_extension('mod_spatialite.dll')

# Criando cursor e ativando spatialite
c = conn.cursor()
c.execute('SELECT load_extension("mod_spatialite.dll")')

# Verificando colunas
c.execute('pragma table_info(cities)')
print(c.fetchall(), '\n')

# Verificando primeira linha
c.execute('SELECT name, AsText(geometry) FROM cities LIMIT 1')
print(c.fetchall())

c.close()
conn.close()


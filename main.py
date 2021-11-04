import pandas as pd
import geopandas as gpd
# from jupyterthemes import jtplot
import matplotlib.pyplot as plt
import plotly.express as px

# jtplot.style(theme='monokai', ticks=True) (Essa maneira de usar temas também não funciona com esse tipo de função de mapa por algum motivo

df = gpd.read_file("rio.json")
print(df.head())

fig = px.choropleth(df,
                   geojson=df.geometry,
                   locations=df.index,
                   color = "name",
                   projection="mercator")

fig.update_layout(
    hovermode='closest',
    title="teste",
    geo = dict(
        # coastlinecolor="#8a8a8a",
        # lakecolor="#8a8a8a",
        # landcolor="#8a8a8a",
        # oceancolor="#8a8a8a",
        # rivercolor="#8a8a8a",
        countrywidth=0,
        center=dict(
                    lat=-22.908333,
                    lon=-43.196388),
        scope='south america',
        projection=dict(
            scale=5
        )
    ),
    # Encontrar maneira de fazer estilos do mapbox funcionar
    # mapbox = dict(
    #             # style options: "basic", "streets", "outdoors", 
    #             # "dark", "satellite", or "satellite-streets","light"
    #             # "open-street-map", "carto-positron", 
    #             # "carto-darkmatter", "stamen-terrain", 
    #             # "stamen-toner" or "stamen-watercolor"
    #             style='dark',
    #             bearing=0,
    #             pitch=0,
    #             accesstoken="pk.eyJ1IjoiYmFycmFmYXMxNSIsImEiOiJja3ZrYWFmZHBicnB4MnZ0OTNrdnNjenNoIn0.Md0bkjH3z7tcOvnzYgz8iw",
    #             zoom=5,
    #             center=dict(
    #                 lat=-22.908333,
    #                 lon=-43.196388))
    )

fig.show()

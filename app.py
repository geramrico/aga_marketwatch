# streamlit_app.py

import streamlit as st
import pandas as pd
from gsheetsdb import connect

# Create a connection object.
conn = connect()

#Columnas
columnas = ["Título",
"Fecha",
"Link",
"Fuente",
"Linea_negocio",
"Ramo",
"Región",
"Audiencia",
"Subcategoría",
"Aseguradora",
"Banca",
"Broker",
"Armadoras",
"Fintech",
"Insurtech",
"Otras industrias",
"Producto",
"Servicio",
"Experiencia",
"Mercado",
"Marca",
"Comunicación",
"Tecnología",
"Innovación",
"Sustentabilidad",
"Alianza",
"Fusion",
"Adquisición",
"Oferta Agresiva",
"Lanzamientos",
"Financieros",
"Enfermedades",
"Cobertura",
"Tag 1",
"Tag 2",
"Tag 3",
"Comentarios",
"Relevancia"]

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query,headers=1)
    rows = rows.fetchall()  
    return rows

@st.experimental_memo
def table_from_query(rows):
    base_dict = []
    for row in rows:
        new_dict = dict(zip(columnas, row))
        base_dict.append(new_dict)

    return pd.DataFrame(base_dict)

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

data = table_from_query(rows)
data = data.sort_values(by="Fecha",ascending=False)


fuentes = st.sidebar.multiselect(label='Fuente',options=data['Fuente'].drop_duplicates())
lineas_negocio = st.sidebar.multiselect(label='Línea de Negocio',options=data['Linea_negocio'].drop_duplicates())
regiones = st.sidebar.multiselect(label='Región',options=data['Región'].drop_duplicates())
ramos = st.sidebar.multiselect(label='Ramo',options=data['Ramo'].drop_duplicates())
audiencias = st.sidebar.multiselect(label='Audiencia',options=data['Audiencia'].drop_duplicates())
subcategorias = st.sidebar.multiselect(label='Subcategoría',options=data['Subcategoría'].drop_duplicates())


filter_query = '''

  (Fuente in @fuentes) or 
  (Linea_negocio in @lineas_negocio) or
  (Región in @regiones) or
  (Ramo in @ramos) or
  (Audiencia in @audiencias) or
  (Subcategoría in @subcategorias)

'''
filter_query = filter_query.replace('\n','')

filtered_data = data.query(filter_query)

if filtered_data.empty:
  st.warning('Selecciona un filtro en la barra lateral para mostrar resultados')

for r in filtered_data.itertuples():
  st.markdown(f'#### {r.Título}')
  st.caption(r.Comentarios)
  st.markdown(f'[Nota]({r.Link})')

  relev = {
    'Baja':'🔹',
    'Media':'🔹🔹',
    'Alta':'🔹🔹🔹',
  }

  if r.Relevancia:
    relevancia = f'Relevancia {relev[r.Relevancia]}'

  st.markdown(f'**{r.Fuente}** | {r.Fecha}')

  st.markdown(f'Region: {r.Región} | Ramo: {r.Ramo} | {r.Audiencia}')




  st.markdown('---')

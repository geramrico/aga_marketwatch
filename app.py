# streamlit_app.py

import streamlit as st
import pandas as pd
from gsheetsdb import connect

st.set_page_config(layout='wide',
        initial_sidebar_state='expanded',
        page_title='Market Watch',
        page_icon='馃摪',)

# Create a connection object.
conn = connect()

#Columnas
columnas = ["T铆tulo",
"Fecha",
"Link",
"Fuente",
"Linea_negocio",
"Ramo",
"Regi贸n",
"Audiencia",
"Subcategor铆a",
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
"Comunicaci贸n",
"Tecnolog铆a",
"Innovaci贸n",
"Sustentabilidad",
"Alianza",
"Fusion",
"Adquisici贸n",
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
lineas_negocio = st.sidebar.multiselect(label='L铆nea de Negocio',options=data['Linea_negocio'].drop_duplicates())
regiones = st.sidebar.multiselect(label='Regi贸n',options=data['Regi贸n'].drop_duplicates())
ramos = st.sidebar.multiselect(label='Ramo',options=data['Ramo'].drop_duplicates())
audiencias = st.sidebar.multiselect(label='Audiencia',options=data['Audiencia'].drop_duplicates())
subcategorias = st.sidebar.multiselect(label='Subcategor铆a',options=data['Subcategor铆a'].drop_duplicates())


filter_query = '''

  (Fuente in @fuentes) or 
  (Linea_negocio in @lineas_negocio) or
  (Regi贸n in @regiones) or
  (Ramo in @ramos) or
  (Audiencia in @audiencias) or
  (Subcategor铆a in @subcategorias)

'''
filter_query = filter_query.replace('\n','')

filtered_data = data.query(filter_query)

if filtered_data.empty:
  st.warning('Selecciona un filtro en la barra lateral para mostrar resultados')

for r in filtered_data.itertuples():
  st.markdown(f'#### {r.T铆tulo}')
  st.caption(r.Comentarios)
  st.markdown(f'[Nota]({r.Link})')

  relev = {
    'Baja':'馃敼',
    'Media':'馃敼馃敼',
    'Alta':'馃敼馃敼馃敼',
  }

  if r.Relevancia:
    relevancia = f'Relevancia {relev[r.Relevancia]}'

  st.markdown(f'**{r.Fuente}** | {r.Fecha}')

  st.markdown(f'Region: {r.Regi贸n} | Ramo: {r.Ramo} | {r.Audiencia}')




  st.markdown('---')

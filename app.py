# streamlit_app.py

import streamlit as st
import pandas as pd
from gsheetsdb import connect

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Market Watch",
    page_icon="📰",
)

# Create a connection object.
conn = connect()

# Columnas
columnas = [
    "Título",
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
    "Tag_1",
    "Tag_2",
    "Tag_3",
    "Comentarios",
    "Relevancia",
]

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


@st.experimental_memo
def table_from_query(rows):
    base_dict = []
    for row in rows:
        new_dict = dict(zip(columnas, row))
        base_dict.append(new_dict)

    return pd.DataFrame(base_dict)


# @st.cache
def list_of(df,column_name):
  return sorted(df[column_name].drop_duplicates())


sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

data = table_from_query(rows)
data = data.sort_values(by="Fecha", ascending=False)


all_tags = list_of(data,"Tag_1") + list_of(data,"Tag_2") + list_of(data,"Tag_3")

fuentes = st.sidebar.multiselect(label="Fuente", options=list_of(data,'Fuente'),on_change=data)
lineas_negocio = st.sidebar.multiselect(label="Línea de Negocio", options=list_of(data,'Linea_negocio'))
regiones = st.sidebar.multiselect(label="Región", options=list_of(data,'Región'))
ramos = st.sidebar.multiselect(label="Ramo", options=list_of(data,'Ramo'))
audiencias = st.sidebar.multiselect(label="Audiencia", options=list_of(data,'Audiencia'))
st.sidebar.write('---')
tags = st.sidebar.multiselect(label="Palabras Clave", options=all_tags)


# ORIGINAL
#region
# filter_query = '''

#   (Fuente in @fuentes) or
#   (Linea_negocio in @lineas_negocio) or
#   (Región in @regiones) or
#   (Ramo in @ramos) or
#   (Audiencia in @audiencias)

# '''
# filter_query = filter_query.replace('\n','')

# filtered_data = data.query(filter_query)
# ORIGINAL

# st.write(fuentes)
# if len(fuentes) > 0:
#     data = data.query("Fuente in @fuentes")

# st.write(lineas_negocio)
# if len(lineas_negocio) > 0:
#     data = data.query("Linea_negocio in @lineas_negocio")

# st.write(regiones)
# if len(regiones) > 0:
#     data = data.query("Región in @regiones")

# st.write(ramos)
# if len(ramos) > 0:
#     data = data.query("Audiencia in @audiencias")
#endregion

if len(fuentes) == 0:
  fuentes = sorted(data["Fuente"].drop_duplicates())
if len(lineas_negocio) == 0:
  lineas_negocio = sorted(data["Linea_negocio"].drop_duplicates())
if len(regiones) == 0:
  regiones = sorted(data["Región"].drop_duplicates())
if len(ramos) == 0:
  ramos = sorted(data["Ramo"].drop_duplicates())
if len(audiencias) == 0:
  audiencias = sorted(data["Audiencia"].drop_duplicates())
if len(tags) == 0:
  tags = all_tags



data = data[
    data["Fuente"].isin(fuentes)
    & data["Ramo"].isin(ramos)
    & data["Linea_negocio"].isin(lineas_negocio)
    & data["Ramo"].isin(ramos)
    & data["Audiencia"].isin(audiencias)

    & (data["Tag_1"].isin(tags)
    | data["Tag_2"].isin(tags)
    | data["Tag_3"].isin(tags))
]

found_data = data.shape[0]
filtered_data = data


st.header('Market Watch')
if filtered_data.empty:
    st.warning("No hay información para los filtros seleccionados")

st.sidebar.info(f"""Se encontraron {found_data} notas""")

for i,r in enumerate(filtered_data.itertuples()):
    st.markdown(f"#### {i+1}. {r.Título}")
    st.caption(r.Comentarios)
    st.markdown(f"[Nota]({r.Link})")

    relev = {
        "Baja": "❗",
        "Media": "❗❗",
        "Alta": "❗❗❗",
    }

    col1,col2 = st.columns(2)

    with col2:
      if r.Relevancia:
          relevancia = f"Relevancia {relev[r.Relevancia]}"
          st.write(relevancia)
      st.markdown(f"**Region:** {r.Región} | **Ramo:** {r.Ramo} | **{r.Audiencia}**")

    with col1:
      st.markdown(f"**{r.Fuente}** | {r.Fecha}")
      f'''**Palabras clave:** {r.Tag_1} - {r.Tag_2} - {r.Tag_3}'''


    st.markdown("---")

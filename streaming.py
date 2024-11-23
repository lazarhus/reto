import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="movies-project-ba5af")

@st.cache_data
def load_products():
    dbName = db.collection("movies")
    docs = dbName.stream()
    data2 = []
    for doc in docs:
        doc_dict = doc.to_dict()
        data2.append(doc_dict)
    df = pd.DataFrame(data2) 
    return df

@st.cache_data
def load_name(data,name):
    filtered_name = data[data['name'].str.contains(name, case=False)]
    return filtered_name

@st.cache_data
def load_data_bysdirector(data,director):
    filtered_data_bydirector = data[data['director'].str.contains(director)]
    return filtered_data_bydirector

data = pd.DataFrame([])
# se establecen las columnas y el orden que tendria en la tabla
columnas = ["name","genre","director","company"]
data = load_products()[columnas]




st.header("Netflix app")
sidebar = st.sidebar
data_load_state = st.text('Loading data...')


mtodos = sidebar.checkbox("Visualizar todos los filmes")
if mtodos:    
    st.subheader("Todos los filmes")
    st.cache_data.clear()
    data = load_products()[columnas]

nameSearch = sidebar.text_input("Titulo del filme")
btnName = sidebar.button("Buscar filme")
if btnName:
    # st.cache_data.clear()
    # data = load_products()[columnas]
    data = load_name(data,nameSearch)  

selected_director = sidebar.selectbox("Seleccionar director", data['director'].unique())
btnDirector = sidebar.button('Filtrar director')
if btnDirector:
    # st.cache_data.clear()
    # data = load_products()[columnas]
    data = load_data_bysdirector(data,selected_director)

mName = sidebar.text_input("Name:")
mCompany = sidebar.selectbox("Company:", data['company'].unique()) 
mDirector = sidebar.selectbox("Director:", data['director'].unique()) 
mGenre =sidebar.selectbox("Genre:", data['genre'].unique())
btnNew = sidebar.button("Crear nuevo filme")
if mName and mCompany and mDirector and mGenre and btnNew:
    doc_ref = db.collection("movies")
    doc_ref.add({
        "name" : mName,
        "genre" : mGenre,
        "director" : mDirector,
        "company" : mCompany
    })
    
    # st.cache_data.clear()
    # data = load_products()[columnas]

# visualiza los datos en el dataframe
if data.empty:
    st.write("No hay datos")
else:    
    data_load_state.text("Done! (using st.cache)")
    if not mtodos:
        count_row = data.shape[0]
        st.write(f"Total de filmes mostrados : {count_row}")
    st.dataframe(data)
    

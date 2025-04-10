import streamlit as st
import dbcreate
import dbpopulate
import localizar

st.set_page_config(page_title="Zoneamento Urbano", layout="wide")

st.title("Sistema de Zoneamento Urbano")

menu = st.sidebar.selectbox(
    "Escolha uma opção:", 
    ["Início", "Criar Banco de Dados", "Popular Banco de Dados", "Pesquisar Uso Permitido"]
)

if menu == "Início":
    st.write("Bem-vindo ao sistema de gerenciamento de zoneamento urbano.")

elif menu == "Criar Banco de Dados":
    if st.button("Criar Banco"):
        dbcreate.criar_banco()
        st.success("Banco de dados criado com sucesso!")

elif menu == "Popular Banco de Dados":
    if st.button("Popular Banco"):
        dbpopulate.popular_banco()
        st.success("Banco de dados populado com sucesso!")

elif menu == "Pesquisar Uso Permitido":
    localizar.pesquisar_uso()
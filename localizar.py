import streamlit as st
import sqlite3

def buscar_usos(tipo_uso):
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()

    query = '''
        SELECT DISTINCT macrozona_codigo, zona_codigo
        FROM usos_permitidos
        WHERE tipo_uso LIKE ? AND permissao = 'Permitido'
    '''
    cursor.execute(query, (f"%{tipo_uso}%",))  # << aqui era o problema!!
    resultados = cursor.fetchall()

    conn.close()
    return resultados

def pesquisar_uso():
    st.header("Pesquisar Uso Permitido")

    tipo_uso_input = st.text_input("Digite o tipo de uso para pesquisar:")

    if st.button("Buscar"):
        if tipo_uso_input:
            resultados = buscar_usos(tipo_uso_input)  # Passa o input para a função
            if resultados:
                st.success(f"Encontramos {len(resultados)} resultado(s):")
                for macrozona, zona in resultados:
                    st.write(f"Macrozona: {macrozona} | Zona: {zona if zona else 'Geral da Macrozona'}")
            else:
                st.warning("Nenhum uso permitido encontrado para essa busca.")
        else:
            st.error("Digite um termo para buscar.")

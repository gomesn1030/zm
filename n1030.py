pip install json folium streamlit_folium

import streamlit as st
import json
import folium
from streamlit_folium import folium_static

# --- 1. Carregamento de dados ---

# Carrega tabela de usos permitidos (atividade -> zonas permitidas/proibidas).
# Aqui usamos um dicionário de exemplo. Em um caso real, poderíamos stscarregar de um arquivo CSV.
usos_permitidos = {
    "Comércio varejista de pequeno porte": {
        "AUAP": "Permitido (exceto SE-04 e SE-05)",
        "AUAS": "Permitido apenas em Faixas Viárias",
        "AUAC": "Proibido",
        "AUAE": "Permitido",
        "AUPA": "Proibido",
        "ARPA": "Permitido (apoio agrícola/turismo)",
        "ARUC": "Permitido (apoio agrícola/turismo)"
    },
    # ... (demais atividades)
}

# Carrega dicionário de parâmetros urbanísticos por zona (dados simplificados).
parametros = {
    "AUAP": {"CAL_max": 4.0, "TO_max": "60%", "altura_max": "45m"},
    "AUAS": {"CAL_max": 2.0, "TO_max": "60%", "altura_max": "sem limite (exceto setores)"},
    "AUAC": {"CAL_max": 1.5, "TO_max": "60%", "altura_max": "??"},   # ... e assim por diante
    "AUAE": {"CAL_max": 1.0, "TO_max": "60%", "altura_max": "??"},
    "AUPA": {"CAL_max": 0.1, "TO_max": "10%", "altura_max": "12m"},
    "ARPA": {"CAL_max": 0.1, "TO_max": "5%",  "altura_max": "??"},
    "ARUC": {"CAL_max": 0.1, "TO_max": "10%", "altura_max": "??"}
}
# Observação: Os valores acima são exemplificativos. 
# Os valores reais devem ser extraídos do Anexo VII para cada zona e setor especial conforme o caso.

# Carrega GeoJSON com as geometrias das zonas de Joinville
with open("joinville_zoneamento.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)


# --- 2. Interface de busca ---

st.title("Consulta de Zoneamento - Joinville (LC 470/2017)")
atividade = st.text_input("Digite a atividade comercial que deseja pesquisar:", "")

# Botão de busca (opcional, pois ao pressionar Enter já submete)
buscar = st.button("Buscar")

# --- 3. Processamento da busca ---

if atividade or buscar:
    # Normalizar entrada para busca (exemplo: capitalizar e remover acentos se necessário)
    termo = atividade.strip().lower()
    # Verifica correspondência exata ou parcial nas atividades conhecidas
    resultados = [ativ for ativ in usos_permitidos.keys() if termo in ativ.lower()]
    
    if len(resultados) == 0:
        st.error("Atividade não encontrada na base de dados da lei.")
    elif len(resultados) > 1 and termo != resultados[0].lower():
        # Se múltiplos resultados, pedir para refinar ou escolher
        st.write(f"Foram encontradas {len(resultados)} atividades que correspondem a '**{atividade}**':")
        for r in resultados:
            st.write(f"- {r}")
        st.info("Por favor, refine a busca pelo nome completo da atividade.")
    else:
        # Se encontrou exatamente uma atividade (ou tomou o primeiro caso termo==resultados[0])
        atividade_encontrada = resultados[0]
        st.subheader(f"Atividade: {atividade_encontrada}")
        
        zonas_perm = usos_permitidos[atividade_encontrada]
        # Filtra apenas as zonas permitidas (não inclui "Proibido")
        zonas_permitidas = {zona: cond for zona, cond in zonas_perm.items() if "Proibido" not in cond}
        
        if not zonas_permitidas:
            st.warning("Esta atividade não é permitida em nenhum zoneamento urbano/rural.")
        else:
            st.markdown("**Zoneamentos que permitem esta atividade:**")
            # Lista zonas e condições
            for zona, cond in zonas_permitidas.items():
                nome_zona = zona  # aqui poderíamos mapear para nome por extenso
                if cond.upper().startswith("PERMITIDO") and cond != "Permitido":
                    # Mostrar condição se houver (exceto, apenas, etc.)
                    st.write(f"- **{zona}**: {cond}")
                else:
                    st.write(f"- **{zona}**: Permitido")
            
            # --- 4. Geração do mapa com Folium ---
            # Configura mapa centrado em Joinville
            center = [-26.304408, -48.848448]  # coordenadas aproximadas centrais
            base_map = folium.Map(location=center, zoom_start=12)
            
            # Adiciona todas as zonas ao mapa: destaque para permitidas, neutro para demais
            for feature in geojson_data["features"]:
                prop = feature["properties"]
                zona = prop.get("zona") or prop.get("Zoneamento") or prop.get("ZONE")  # diferentes possib. de chave
                geom = feature["geometry"]
                
                if zona in zonas_permitidas:
                    # Estilo para zonas permitidas (e popup com parâmetros)
                    texto_popup = f"<b>{zona}</b>: "
                    if zona in parametros:
                        p = parametros[zona]
                        texto_popup += (f"CAL={p['CAL_max']}, TO={p['TO_max']}, Altura máx={p['altura_max']}")
                    else:
                        texto_popup += "parâmetros conforme lei."
                    
                    folium.GeoJson(
                        geom,
                        name=zona,
                        style_function=lambda x, col="#228B22": {'fillColor': col, 'color': col, 'fillOpacity': 0.5, 'weight': 1},
                        tooltip=folium.Tooltip(f"{zona} (permitido)"),
                        popup=folium.Popup(texto_popup, max_width=300)
                    ).add_to(base_map)
                else:
                    # Estilo para zonas não permitidas (contorno cinza sem popup)
                    folium.GeoJson(
                        geom,
                        style_function=lambda x: {'fillColor': 'gray', 'color': 'gray', 'fillOpacity': 0.1, 'weight': 0.5}
                    ).add_to(base_map)
            
            # Exibe mapa no Streamlit
            folium_static(base_map, width=700, height=500)

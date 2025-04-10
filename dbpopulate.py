import streamlit as st
import sqlite3

# Função para popular o banco de dados
def popular_banco():
    conn = sqlite3.connect('zoneamento.db')
    cursor = conn.cursor()

    cursor.executescript('''
        -- Inserir macrozonas
        INSERT OR IGNORE INTO macrozona (codigo, descricao) VALUES
            ('ARPA', 'Área Rural de Proteção Ambiental'),
            ('ARUC', 'Área Rural de Utilização Controlada'),
            ('AUAP', 'Área Urbana de Adensamento Prioritário'),
            ('AUAS', 'Área Urbana de Adensamento Secundário'),
            ('AUAC', 'Área Urbana de Adensamento Controlado'),
            ('AUAE', 'Área Urbana de Adensamento Especial'),
            ('AUPA', 'Área Urbana de Proteção Ambiental');

        -- Inserir zonas
        INSERT OR IGNORE INTO zona (codigo, nome, macrozona_codigo) VALUES
            ('SA-01', 'Setor de Adensamento Prioritário 01 (Centro)', 'AUAP'),
            ('SA-02', 'Setor de Adensamento Prioritário 02 (Norte/Sul)', 'AUAP'),
            ('SA-03', 'Setor de Adensamento Secundário', 'AUAS'),
            ('SA-04', 'Setor de Adensamento Controlado', 'AUAC'),
            ('SA-05', 'Setor de Adensamento Especial', 'AUAE'),
            ('SE-01', 'Setor Especial de Interesse Cultural', 'AUAP'),
            ('SE-02', 'Setor Especial de Interesse Público', 'AUAP'),
            ('SE-03', 'Setor Especial de Interesse Educacional', 'AUAS'),
            ('SE-04', 'Setor Especial de Conservação de Morros', NULL),
            ('SE-05', 'Setor Especial de Conservação de Várzeas', NULL),
            ('SE-06', 'Setor Especial de Interesse Industrial', 'AUAC'),
            ('SE-06A', 'Setor Especial de Interesse Industrial Misto', 'AUAC'),
            ('SE-07', 'Setor Especial 07 (índices definidos por lei específica)', NULL),
            ('SE-08', 'Setor Especial de Centralidade Urbana', NULL),
            ('SE-09', 'Setor Especial de Interesse de Segurança Pública', 'AUAS');

        -- Inserir parametros_urbanisticos (parcial; '?' nos gabaritos precisam ser definidos manualmente depois)
        INSERT OR IGNORE INTO parametros_urbanisticos (macrozona_codigo, zona_codigo, coeficiente_aprov, gabarito_maximo, area_minima_lote, taxa_ocupacao_max) VALUES
            ('AUAP','SA-01', 4.0, 45, 240, 0.60),
            ('AUAP','SA-02', 3.0, 25, 240, 0.60),
            ('AUAS','SA-03', 2.0, 15, 240, 0.60),
            ('AUAC','SA-04', 1.5, 9,  240, 0.60),
            ('AUAE','SA-05', 1.0, 9,  450, 0.60),
            ('AUPA',NULL,   0.1, 9, 5000, 0.10),
            ('ARPA',NULL,   0.1, 9, 20000, 0.05),
            ('ARUC',NULL,   0.1, 9, 20000, 0.10),
            ('AUAP','SE-01', 4.0, 30, 240, 0.60),
            ('AUAP','SE-02', 2.0, 15, 240, 0.60),
            ('AUAS','SE-03', 1.0, 30, 240, 0.60),
            ('AUAP','SE-04', 0.1, 9, 240, 0.10),
            ('AUAS','SE-04', 0.1, 9, 240, 0.10),
            ('AUAC','SE-04', 0.1, 9, 240, 0.10),
            ('AUAE','SE-04', 0.1, 9, 450, 0.10),
            ('AUPA','SE-04', 0.1, 9, 5000, 0.10),
            ('AUAP','SE-05', 0.1, 9, 240, 0.10),
            ('AUAS','SE-05', 0.1, 9, 240, 0.10),
            ('AUAC','SE-05', 0.1, 9, 240, 0.10),
            ('AUAE','SE-05', 0.1, 9, 450, 0.10),
            ('AUPA','SE-05', 0.1, 9, 5000, 0.10);

        -- Inserir usos_permitidos
        INSERT OR IGNORE INTO usos_permitidos (macrozona_codigo, zona_codigo, tipo_uso, porte, cnae, permissao) VALUES
            ('AUAP', 'SA-01', 'Residencial Unifamiliar', NULL, NULL, 'Permitido'),
            ('AUAP', 'SA-01', 'Residencial Multifamiliar', NULL, NULL, 'Permitido'),
            ('AUPA', NULL, 'Residencial Multifamiliar', NULL, NULL, 'Proibido'),
            ('ARPA', NULL, 'Residencial Unifamiliar', NULL, NULL, 'Permitido'),
            ('AUAP', 'SA-02', 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Permitido'),
            ('AUAS', 'SA-03', 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Condicionado'),
            ('AUAC', 'SA-04', 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Proibido'),
            ('ARPA', NULL, 'Comércio Varejista', 'Pequeno Porte', '45 e 47', 'Condicionado'),
            ('AUAP', 'SA-01', 'Comércio Varejista', 'Médio Porte', '47.3', 'Permitido'),
            ('AUAS', 'SA-03', 'Comércio Varejista', 'Médio Porte', '47.3', 'Condicionado'),
            ('AUAC', 'SA-04', 'Comércio Varejista', 'Médio Porte', '47.3', 'Proibido'),
            ('AUPA', NULL, 'Comércio Varejista', 'Médio Porte', NULL, 'Proibido'),
            ('AUAC', 'SA-04', 'Atividade Industrial', 'Pequeno Porte', NULL, 'Permitido'),
            ('AUAS', 'SA-03', 'Atividade Industrial', 'Pequeno Porte', NULL, 'Condicionado'),
            ('AUAP', 'SA-02', 'Atividade Industrial', 'Pequeno Porte', NULL, 'Proibido'),
            ('AUPA', NULL, 'Atividade Industrial', 'Pequeno Porte', NULL, 'Proibido');

        -- Inserir faixa_especial
        INSERT OR IGNORE INTO faixa_especial (codigo, descricao) VALUES
            ('FV', 'Faixa Viária'),
            ('FR', 'Faixa Rodoviária');

        -- Inserir zona_faixa_especial
        INSERT OR IGNORE INTO zona_faixa_especial (zona_codigo, faixa_codigo) VALUES
            ('SA-01', 'FV'),
            ('SA-02', 'FV'),
            ('SA-02', 'FR'),
            ('SA-03', 'FV'),
            ('SA-03', 'FR'),
            ('SA-04', 'FR'),
            ('SA-05', 'FV');
    ''')

    conn.commit()
    conn.close()

# --- Streamlit App ---

st.title("Popular Banco de Dados de Zoneamento")

st.write("Este app insere dados padrões nas tabelas do banco 'zoneamento.db'.")

if st.button("Popular Banco de Dados"):
    popular_banco()
    st.success("Banco de dados populado com sucesso!")
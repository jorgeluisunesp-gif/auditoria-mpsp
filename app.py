# -----------------------------------------------------------------------------
# PASSO 1: INSTALAÇÃO DAS BIBLIOTECAS (Execute esta célula no Colab)
# -----------------------------------------------------------------------------
import os

# Instala o Streamlit
os.system('pip install streamlit -q')

# Cria o arquivo do aplicativo (app.py)
# Tudo o que estiver abaixo de %%writefile será salvo como um arquivo Python
# -----------------------------------------------------------------------------

with open("app.py", "w", encoding="utf-8") as f:
    f.write('''
import streamlit as st
import pandas as pd
import json
import os
import glob

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Auditoria MPSP 4.0",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f3ff;
        border-bottom: 2px solid #0068c9;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data(filename):
    """Carrega JSON e converte para DataFrame com tratamento de erro"""
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao ler {filename}: {e}")
        return None

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Brasao_do_estado_de_Sao_Paulo.svg/100px-Brasao_do_estado_de_Sao_Paulo.svg.png", width=80)
    st.title("Auditoria Ativa")
    st.markdown("---")
    st.markdown("**Pesquisador:** Jorge Luis Carneiro Junior")
    st.markdown("**Grupo:** Democracia e Combate à Corrupção (ESMP)")
    st.markdown("---")
    st.info("Este painel apresenta os resultados dos algoritmos de detecção de fraudes (Red Flags) aplicados ao AUDESP e RFB.")

# --- TÍTULO PRINCIPAL ---
st.title("🕵️ Painel de Inteligência: Fiscalização de Contratos")
st.markdown("Visualize, filtre e audite as anomalias detectadas pelos algoritmos de Big Data.")

# --- ABAS (TABS) PARA CADA RED FLAG ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚩 RF1: Competitividade", 
    "🚩 RF2: Fracionamento", 
    "🚩 RF3: Clubes/Cartéis", 
    "🚩 RF4: Empresas Novas", 
    "🚩 RF5: Sócios/Vínculos"
])

# ==============================================================================
# ABA 1: RED FLAG 1 (Competitividade)
# ==============================================================================
with tab1:
    st.header("Red Flag 1: Atipicidade Competitiva (Participante Único)")
    df_rf1 = load_data("redflag1.json") # Assumindo nome do arquivo
    
    if df_rf1 is not None:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            municipio = st.selectbox("Filtrar Município (RF1):", ["Todos"] + list(df_rf1['Municipio'].unique()))
        with col2:
            search = st.text_input("Buscar Fornecedor (RF1):", "")

        df_filtered = df_rf1.copy()
        if municipio != "Todos":
            df_filtered = df_filtered[df_filtered['Municipio'] == municipio]
        if search:
            df_filtered = df_filtered[df_filtered['licitante'].str.contains(search, case=False, na=False)]

        # Métricas
        m1, m2 = st.columns(2)
        m1.metric("Licitantes Únicos", len(df_filtered))
        
        # Tabela
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.warning("Arquivo 'redflag1.json' não encontrado. Faça o upload para visualizar.")

# ==============================================================================
# ABA 2: RED FLAG 2 (Fracionamento)
# ==============================================================================
with tab2:
    st.header("Red Flag 2: Fracionamento de Despesa (Dispensas Acumuladas)")
    df_rf2 = load_data("redflag2.json")
    
    if df_rf2 is not None:
        col1, col2 = st.columns(2)
        with col1:
            search_entidade = st.text_input("Buscar Entidade/Órgão:", "")
        with col2:
            search_empresa = st.text_input("Buscar Empresa Beneficiada:", "")

        df_show = df_rf2.copy()
        if search_entidade:
            df_show = df_show[df_show['Entidade'].str.contains(search_entidade, case=False, na=False)]
        if search_empresa:
            df_show = df_show[df_show['Empresa'].str.contains(search_empresa, case=False, na=False)]

        st.dataframe(df_show, use_container_width=True)
    else:
        st.warning("Arquivo 'redflag2.json' não encontrado.")

# ==============================================================================
# ABA 3: RED FLAG 3 (Clubes)
# ==============================================================================
with tab3:
    st.header("Red Flag 3: Grupos de Interação Recorrente (Clubes)")
    df_rf3 = load_data("redflag3.json")
    
    if df_rf3 is not None:
        st.markdown("Identificação de grupos de empresas que participam juntas repetidamente.")
        
        # Filtro por tamanho do grupo
        min_size = st.slider("Tamanho Mínimo do Grupo:", 4, 20, 4)
        df_show = df_rf3[df_rf3['Tamanho_do_Grupo'] >= min_size]
        
        st.dataframe(df_show, use_container_width=True)
    else:
        st.warning("Arquivo 'redflag3.json' não encontrado.")

# ==============================================================================
# ABA 4: RED FLAG 4 (Empresas Novas)
# ==============================================================================
with tab4:
    st.header("Red Flag 4: Maturidade Empresarial (Empresas Recém-Criadas)")
    
    # Tenta carregar 4.1 ou 4.2
    df_rf4_1 = load_data("redflag4.1.json")
    df_rf4_2 = load_data("redflag4.2.json")
    
    tipo_analise = st.radio("Selecione o Tipo de Análise:", ["4.1 - Viagem no Tempo (Data Negativa)", "4.2 - Bebês Gigantes (Recém-Criadas)"])
    
    if tipo_analise == "4.1 - Viagem no Tempo (Data Negativa)":
        if df_rf4_1 is not None:
            st.error("🚨 ATENÇÃO: Contratos assinados ANTES da abertura da empresa.")
            st.dataframe(df_rf4_1, use_container_width=True)
        else:
            st.warning("Arquivo 'redflag4.1.json' não encontrado.")
            
    else:
        if df_rf4_2 is not None:
            st.warning("⚠️ ALERTA: Empresas com menos de 6 meses ganhando contratos altos.")
            st.dataframe(df_rf4_2, use_container_width=True)
        else:
            st.warning("Arquivo 'redflag4.2.json' não encontrado.")

# ==============================================================================
# ABA 5: RED FLAG 5 (Sócios)
# ==============================================================================
with tab5:
    st.header("Red Flag 5: Vínculos Societários e Conluio")
    df_rf5_1 = load_data("redflag5.1.json")
    df_rf5_2 = load_data("redflag5.2.json")
    
    dataset = st.selectbox("Selecione a Base:", ["5.1 - Simulação Competitiva", "5.2 - Fraude Cota LC 123"])
    
    df_target = df_rf5_1 if "5.1" in dataset else df_rf5_2
    
    if df_target is not None:
        socio_search = st.text_input("Buscar pelo Nome do Sócio:", "")
        if socio_search:
            df_target = df_target[df_target['Socio_Comum'].str.contains(socio_search, case=False, na=False)]
            
        st.dataframe(df_target, use_container_width=True)
    else:
        st.warning(f"Arquivo JSON para {dataset} não encontrado.")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Sistema desenvolvido em Python com Streamlit. Dados extraídos do BigQuery (AUDESP + RFB).")
    ''')

# -----------------------------------------------------------------------------
# PASSO 2: EXECUTAR O PAINEL E GERAR O LINK PÚBLICO
# -----------------------------------------------------------------------------
print("Instalando dependências e iniciando o túnel...")
import urllib
# Obtém o IP externo para senha do LocalTunnel (se necessário)
print("----------------------------------------------------------------")
print("SENHA DO TUNEL (Copie este IP se for solicitado): ", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n"))
print("----------------------------------------------------------------")
print("Clique no link abaixo que termina em 'loca.lt' para abrir o painel:")

# Executa o Streamlit em background e abre o túnel na porta 8501
get_ipython().system_raw('streamlit run app.py & npx localtunnel --port 8501 &')
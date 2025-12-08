# -----------------------------------------------------------------------------
# PASSO 1: INSTALAÇÃO E CONFIGURAÇÃO (Execute esta célula no Colab)
# -----------------------------------------------------------------------------
import os
import time
import urllib.request

# Função para executar comandos no estilo do Colab
def run_shell(command):
    try:
        get_ipython().system(command)
    except:
        os.system(command)

print("⏳ Instalando bibliotecas necessárias (Streamlit)...")
run_shell('pip install streamlit -q')
print("✅ Instalação concluída!")

# -----------------------------------------------------------------------------
# PASSO 2: CRIAÇÃO DO ARQUIVO DO APLICATIVO (app.py)
# -----------------------------------------------------------------------------
print("📝 Criando o arquivo do painel (app.py)...")

code_content = '''
import streamlit as st
import pandas as pd
import json
import os

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
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO DE CARREGAMENTO DE DADOS ---
@st.cache_data
def load_data(filename):
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
    st.info("Painel de Inteligência para detecção de fraudes em licitações.")

# --- TÍTULO PRINCIPAL ---
st.title("🕵️ Painel de Inteligência: Fiscalização de Contratos")
st.markdown("Visualize, filtre e audite as anomalias detectadas pelos algoritmos de Big Data.")

# --- ABAS (TABS) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚩 RF1: Competitividade", 
    "🚩 RF2: Fracionamento", 
    "🚩 RF3: Clubes/Cartéis", 
    "🚩 RF4: Empresas Novas", 
    "🚩 RF5: Sócios/Vínculos"
])

# ABA 1: COMPETITIVIDADE
with tab1:
    st.header("Red Flag 1: Atipicidade Competitiva")
    df = load_data("redflag1.json")
    if df is not None:
        filtro = st.text_input("Buscar Fornecedor (RF1):", "")
        if filtro:
            df = df[df['licitante'].str.contains(filtro, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Arquivo redflag1.json não encontrado.")

# ABA 2: FRACIONAMENTO
with tab2:
    st.header("Red Flag 2: Fracionamento de Despesa")
    df = load_data("redflag2.json")
    if df is not None:
        entidade = st.text_input("Buscar Órgão:", "")
        if entidade:
            df = df[df['Entidade'].str.contains(entidade, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Arquivo redflag2.json não encontrado.")

# ABA 3: CLUBES
with tab3:
    st.header("Red Flag 3: Grupos de Interação (Clubes)")
    df = load_data("redflag3.json")
    if df is not None:
        tamanho = st.slider("Tamanho Mínimo do Grupo:", 4, 20, 4)
        st.dataframe(df[df['Tamanho_do_Grupo'] >= tamanho], use_container_width=True)
    else:
        st.warning("Arquivo redflag3.json não encontrado.")

# ABA 4: EMPRESAS NOVAS
with tab4:
    st.header("Red Flag 4: Maturidade Empresarial")
    tipo = st.radio("Tipo:", ["4.1 - Viagem no Tempo", "4.2 - Bebês Gigantes"])
    arquivo = "redflag4.1.json" if "4.1" in tipo else "redflag4.2.json"
    df = load_data(arquivo)
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Arquivo {arquivo} não encontrado.")

# ABA 5: SÓCIOS
with tab5:
    st.header("Red Flag 5: Vínculos Societários")
    tipo = st.selectbox("Base:", ["5.1 - Simulação", "5.2 - Fraude Cota"])
    arquivo = "redflag5.1.json" if "5.1" in tipo else "redflag5.2.json"
    df = load_data(arquivo)
    if df is not None:
        socio = st.text_input("Buscar Sócio:", "")
        if socio:
            df = df[df['Socio_Comum'].str.contains(socio, case=False, na=False)]
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Arquivo {arquivo} não encontrado.")
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(code_content)

print("✅ Arquivo app.py criado com sucesso.")

# -----------------------------------------------------------------------------
# PASSO 3: INICIAR O SERVIDOR E O TÚNEL
# -----------------------------------------------------------------------------
print("\n🚀 Iniciando o servidor Streamlit...")

# Obter o IP Público para usar como SENHA do túnel
ipv4 = urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip("\n")
print(f"\n⚠️ IMPORTANTE: A senha para acessar o site é o IP abaixo:")
print(f"👉 \033[1m{ipv4}\033[0m 👈 (Copie este número!)\n")

# Executa o Streamlit em background
get_ipython().system_raw('streamlit run app.py &')

# Aguarda um pouco para o Streamlit iniciar
time.sleep(3)

# Inicia o túnel (npx localtunnel)
print("🔗 Clique no link abaixo e cole o IP acima na caixa 'Tunnel Password':")
get_ipython().system_raw('npx localtunnel --port 8501 &')

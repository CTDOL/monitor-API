import streamlit as st
import json
from google.oauth2 import service_account
from google.cloud import monitoring_v3
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Monitor Gemini", layout="centered")
st.title("Consumo da API Gemini 🚀")

# 1. Carregar Credenciais dos SECRETS do Streamlit (Muito Seguro!)
try:
    # Lemos a string JSON que vamos configurar na plataforma do Streamlit
    gcp_json_str = st.secrets["GCP_CREDENTIALS"]
    cred_dict = json.loads(gcp_json_str)
    
    # Criar a credencial oficial do Google
    credentials = service_account.Credentials.from_service_account_info(cred_dict)
    project_id = cred_dict["project_id"]
    
    st.success(f"Autenticado com sucesso no projeto: {project_id}")
except Exception as e:
    st.error("Erro de Autenticação. Verifique os Secrets no painel do Streamlit.")
    st.stop()

# 2. Configurar o Cliente de Monitorização
@st.cache_resource
def get_monitoring_client():
    return monitoring_v3.MetricServiceClient(credentials=credentials)

client = get_monitoring_client()
project_name = f"projects/{project_id}"

# 3. Desenhar o Velocímetro (Gauge) com Plotly
def draw_gauge(value, max_val=15):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Requisições por Segundo (1/s)"},
        gauge = {
            'axis': {'range': [None, max_val]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [0, 8], 'color': "lightgreen"},
                {'range': [8, 12], 'color': "yellow"},
                {'range': [12, max_val], 'color': "red"}],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# 4. Lógica para buscar os dados (Esqueleto)
# Aqui entraria a query à métrica exacta do Cloud Monitoring.
# Como a API do Monitoring exige um intervalo de tempo (ex: últimos 5 mins), 
# deixo aqui o placeholder para o velocímetro renderizar na perfeição:
valor_atual = 0 # Substituir pela chamada real a client.list_time_series()

draw_gauge(valor_atual)

# Botão para atualizar
if st.button("Atualizar Métrica"):
    st.rerun()
import streamlit as st
from datetime import datetime, timedelta

# Lead times
lead_time_data = {
    ("MG", "AM"): 30,
    ("MG", "BA"): 9,
    ("MG", "GO"): 8,
    ("MG", "MA"): 16,
    ("MG", "MG"): 1,
    ("MG", "PB"): 10,
    ("SP", "AM"): 34,
    ("SP", "BA"): 13,
    ("SP", "GO"): 12,
    ("SP", "MA"): 20,
    ("SP", "MG"): 5,
    ("SP", "PB"): 14,
    ("PR", "AM"): 34,
    ("PR", "BA"): 13,
    ("PR", "GO"): 12,
    ("PR", "MG"): 4,
    ("PR", "PB"): 14,
    ("SC", "AM"): 35,
    ("SC", "BA"): 14,
    ("SC", "GO"): 13,
    ("SC", "MG"): 5,
    ("SC", "PB"): 15,
    ("GO", "AM"): 34,
    ("GO", "BA"): 9,
    ("GO", "MG"): 5,
    ("GO", "PB"): 10,
    ("CONT", "GO"): 12,
    ("CONT", "MG"): 5,
    ("CONT", "AM"): 34,
    ("CONT", "PB"): 14,
    ("CONT", "BA"): 13
}

filiais_origem = sorted(list(set([
    origem for origem, _ in lead_time_data.keys()
    if origem not in ["PR", "GO"]
])))

filiais_origem_map = {
    "MG": "Uberlândia - MG",
    "SP": "Guarulhos - SP",
    "SC": "Palhoça - SC",
    "CONT": "Contagem - MG"
}

filiais_destino = sorted(list(set([dest for _, dest in lead_time_data.keys()])))

# Função para calcular dias úteis
def adicionar_dias_uteis(data_inicial, dias):
    data = data_inicial
    while dias > 0:
        data += timedelta(days=1)
        if data.weekday() < 5:
            dias -= 1
    return data

# Ajuste para destinos com regras especiais
def ajustar_para_fim_de_semana(data, destino):
    if destino in ["BA", "PB", "GO", "AM", "MA"]:
        while data.weekday() != 5:
            data += timedelta(days=1)
    elif destino == "MG":
        while data.weekday() != 6:
            data += timedelta(days=1)
    return data

# Interface principal
st.title("Calculadora de Lead Time C3")

col1, col2 = st.columns(2)
with col1:
    origem_sigla = st.selectbox("Filial de Origem", filiais_origem, format_func=lambda x: filiais_origem_map.get(x, x))
with col2:
    destino = st.selectbox("Filial de Destino (UF)", filiais_destino)

# Campo para data base
data_base = st.date_input("Data base para cálculo", datetime.today())

# Botão para calcular
if st.button("Calcular Data de Agendamento"):
    dias_lead_time = lead_time_data.get((origem_sigla, destino))

    if dias_lead_time:
        data_prevista = adicionar_dias_uteis(data_base, dias_lead_time)
        data_ajustada = ajustar_para_fim_de_semana(data_prevista, destino)

        st.success(f"A carga deve ser agendada para: **{data_ajustada.strftime('%d/%m/%Y')}**")
    else:
        st.warning("Não há lead time cadastrado para essa combinação de origem e destino.")

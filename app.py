import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.header("Dashboard de Análise de Desempenho")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados.csv")
    return df

df = carregar_dados() 

with st.sidebar:
    st.subheader("Filtros")
    
    opcoes_dept = df["departamento"].unique()
    deptos_escolhidos = st.multiselect(
        "Departamentos:", 
        opcoes_dept,
        default=opcoes_dept 
    )
    
    opcoes_regiao = df["regiao"].unique()
    regioes_escolhidas = st.multiselect(
        "Regiões:", 
        opcoes_regiao,
        default=opcoes_regiao
    )

    sal_min = int(df['salario_mensal'].min())
    sal_max = int(df['salario_mensal'].max())

    faixa_salarial_escolhida = st.slider(
        "Filtrar por salário (R$):",
        min_value=sal_min,
        max_value=sal_max,
        value=(sal_min, sal_max) 
    )

min_sal = faixa_salarial_escolhida[0]
max_sal = faixa_salarial_escolhida[1]

df_filtrado = df[
    (df['departamento'].isin(deptos_escolhidos)) &
    (df['regiao'].isin(regioes_escolhidas)) &
    (df['salario_mensal'] >= min_sal) &
    (df['salario_mensal'] <= max_sal)
]


st.subheader(f"Distribuição de Salários (Dados Filtrados)")
st.write(f"Mostrando {len(df_filtrado)} funcionários de um total de {len(df)}.")

if not df_filtrado.empty:
    fig, ax = plt.subplots()
    
    ax.hist(df_filtrado['salario_mensal'], bins=10, edgecolor='black')
    ax.set_xlabel("Salário Mensal")
    ax.set_ylabel("Nº de Funcionários")
    
    # Adicionar linhas verticais mostrando a faixa selecionada no slider
    ax.axvline(min_sal, color='red', linestyle='--', linewidth=2)
    ax.axvline(max_sal, color='red', linestyle='--', linewidth=2)
    
    st.pyplot(fig, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")


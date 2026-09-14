import streamlit as st
import pandas as pd

pd.DataFrame({"Gerador": ["Edificio Piazza São Pietro", "Vila Borguese", "Edificio Honduras"], "Aluminio":100 , "Plastico": 200, "Papel": 300 ,"Horário Chegada": ["08:00", "10:00", "12:00"],"Preço Estimado Material": [1000, 2000, 3000], "Quem vai trazer": ["Roberto", "Claudio", "Claudio Logistics"]})

df = pd.DataFrame({"Gerador": ["Edificio Piazza São Pietro", "Vila Borguese", "Edificio Honduras"],  "Aluminio":[100,200,300] , "Plastico": [400,500,600], "Papel": [700,800,900] ,"Horário Chegada": ["08:00", "10:00", "12:00"],"Preço Estimado Material": [1000, 2000, 3000], "Quem vai trazer": ["Roberto", "Claudio", "Claudio Logistics"], "Pagamento Transportador": [200, 300, 3000], "Pagamento Gerador": [800, 2000-300, 0], "Pedido": ["1001", "1002", "1003"], "Status": ["Não Iniciado", "Iniciado", "Inspeção"]})

df_banco = pd.read_excel("teste_banco_recicladoras.xlsx")


st.title("Recicladora Ousadia e Alegria")
# st.header("Entregas de Hoje")

## Filtros dinamicos( In progress)
col1, col2, col3, col4 = st.columns(4)
col1.selectbox("O que deseja Filtrar", list(df["Gerador"].unique()), key="col1")
col2.selectbox("O que deseja Filtrar", [0,2,34,4], key="col2")
col3.selectbox("O que deseja Filtrar", list(df["Horário Chegada"].unique()), key="col3")


st.header("Pedidos de Hoje")

for index, row in df.iterrows():

    col1, col2, col3, col4,col5 = st.columns([1, 3, 2, 1, 1])

    col1.write(row["Pedido"])
    col2.write(row["Gerador"])
    col3.write(row["Horário Chegada"])
    col4.write(f"Status: {row['Status']}")

    if col5.button("Abrir", key=f"pedido_{row['Pedido']}"):
        st.session_state["pedido_selecionado"] = row["Pedido"]


if "pedido_selecionado" in st.session_state:

    pedido = st.session_state["pedido_selecionado"]

    pedido_data = df[df["Pedido"] == pedido].iloc[0]

    st.divider()

    st.header(f"Pedido #{pedido}")
    if pedido_data["Status"] == "Não Iniciado":
        fill = "style A fill:#ff4b4b,stroke:#b30000,stroke-width:2px,color:white"
    elif pedido_data["Status"] == "Iniciado":
        fill = "style B fill:green,stroke-width:2px,color:white"
    elif pedido_data["Status"] == "Entregue":
        fill = "style C fill:green,stroke-width:2px,color:white"
    elif pedido_data["Status"] == "Inspeção":
        fill = "style D fill:green,stroke-width:2px,color:white"
    elif pedido_data["Status"] == "Pagamento":
        fill = "style E fill:green,stroke-width:2px,color:white"
    else:
        fill = "style F fill:green,stroke-width:2px,color:white"
    st.mermaid_chart(f"""
    graph LR
        A[Não Iniciado] --> B[Iniciado]
        B --> C[Entregue]
        C --> D[Inspeção]
        D --> E[Pagamento]
        E --> F[Finalizado]


        {fill}
""")

    st.write("Gerador:", pedido_data["Gerador"])
    st.write("Horário:", pedido_data["Horário Chegada"])
    st.write("Alumínio:", pedido_data["Aluminio"], "kg")
    st.write("Plástico:", pedido_data["Plastico"], "kg")
    st.write("Papel:", pedido_data["Papel"], "kg")
    st.write("Transportador:", pedido_data["Quem vai trazer"])
    st.write("Pagamento ao Transportador: R$", pedido_data["Pagamento Transportador"])
    st.write("Pagamento ao Gerador: R$", pedido_data["Pagamento Gerador"])
    st.header("Fluxo do Pedido")
    st.mermaid_chart(f"""
    graph LR
        A["{pedido_data['Gerador']}"] --> B["{pedido_data['Quem vai trazer']}"]
        B --> C[asdasdasd]
""")





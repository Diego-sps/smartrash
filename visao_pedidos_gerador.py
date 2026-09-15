import streamlit as st
import pandas as pd

st.title("Visão Entregas Gerador")
st.subheader("Recicladora Ousadia e Alegria")


df = pd.DataFrame(
    {
        "Gerador": [
            "Recicladora Ousadia e Alegria",
            "Edificio Piazza São Pietro",
            "Vila Borguese",
            "Edificio Honduras",
        ],
        "Aluminio": [100, 200, 300, 400],
        "Plastico": [50, 400, 500, 600],
        "Papel": [80, 700, 800, 900],
        "Horário Chegada": ["08:00", "10:00", "12:00", "14:00"],
        "Preço Estimado Material": [1200, 1000, 2000, 3000],
        "Quem vai trazer": ["Transportadora Sol", "Roberto", "Claudio", "Claudio Logistics"],
        "Pagamento Transportador": [250, 200, 300, 3000],
        "Pagamento Gerador": [950, 800, 1700, 0],
        "Pedido": ["1001", "1002", "1003", "1004"],
        "Status": ["Não Iniciado", "Iniciado", "Inspeção", "Pagamento"],
    }
)

st.caption("Pedidos enviados pelo gerador")

for index, row in df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([1.2, 2.5, 2, 1.6, 1.2])

    col1.write(row["Pedido"])
    col2.write(row["Gerador"])
    col3.write(f"{row['Aluminio']} kg de alumínio")
    col4.write(f"Status: {row['Status']}")

    if col5.button("Abrir", key=f"pedido_{row['Pedido']}"):
        st.session_state["pedido_selecionado"] = row["Pedido"]

if "pedido_selecionado" in st.session_state:
    pedido = st.session_state["pedido_selecionado"]
    pedido_data = df[df["Pedido"] == pedido].iloc[0]

    st.divider()
    st.header(f"Pedido #{pedido}")

    status_sequence = {
        "Não Iniciado": "A",
        "Iniciado": "B",
        "Entregue": "C",
        "Inspeção": "D",
        "Pagamento": "E",
        "Finalizado": "F",
    }

    current_status = pedido_data["Status"]
    active_node = status_sequence.get(current_status, "A")
    style_map = {
        "A": "style A fill:#ff4b4b,stroke:#b30000,stroke-width:2px,color:white",
        "B": "style B fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:white",
        "C": "style C fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:white",
        "D": "style D fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:white",
        "E": "style E fill:#22c55e,stroke:#15803d,stroke-width:2px,color:white",
        "F": "style F fill:#16a34a,stroke:#166534,stroke-width:2px,color:white",
    }

    st.mermaid_chart(
        f"""
        graph LR
            A[Pedido enviado] --> B[Pesagem e coleta]
            B --> C[Entrega no destino]
            C --> D[Conferência]
            D --> E[Pagamento integral]
            E --> F[Pedido concluído]

            {style_map.get(active_node, 'style A fill:#ff4b4b,stroke:#b30000,stroke-width:2px,color:white')}
        """
    )

    st.write("Gerador:", pedido_data["Gerador"])
    st.write("Horário:", pedido_data["Horário Chegada"])
    st.write("Alumínio:", pedido_data["Aluminio"], "kg")
    st.write("Plástico:", pedido_data["Plastico"], "kg")
    st.write("Papel:", pedido_data["Papel"], "kg")
    st.write("Transportador:", pedido_data["Quem vai trazer"])
    st.write("Pagamento ao Transportador: R$", pedido_data["Pagamento Transportador"])
    st.write("Pagamento ao Gerador: R$", pedido_data["Pagamento Gerador"])

    st.header("Acompanhamento do pedido")
    st.mermaid_chart(
        f"""
        graph LR
            A[Pedido enviado] --> B[Material em trânsito]
            B --> C[Recebimento confirmado]
            C --> D[Pagamento integral confirmado]
            D --> E[Pedido finalizado]
        """
    )

st.table(df)
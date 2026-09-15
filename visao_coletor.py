import streamlit as st
import pandas as pd
from streamlit_mermaid import st_mermaid


st.title("🚚 Corridas disponíveis")

st.subheader("Encontre uma corrida para realizar")


# =========================================================
# DADOS SIMULADOS
# =========================================================

corridas = [
    {
        "ID": "C001",
        "Inicio": "08:00",
        "Fim": "11:30",
        "Peso": 600,
        "Paradas": 3,
        "Pagamento": 180.00,
        "Origem": "Mooca",
        "Destino": "Recicladora Ousadia e Alegria",
        "Status": "Disponível",

        "rota": [
            ("Edifício Piazza São Pietro", "100 kg Alumínio"),
            ("Vila Borguese", "300 kg Papelão"),
            ("Edifício Honduras", "200 kg Plástico")
        ]
    },

    {
        "ID": "C002",
        "Inicio": "10:00",
        "Fim": "14:00",
        "Peso": 450,
        "Paradas": 2,
        "Pagamento": 150.00,
        "Origem": "Mooca",
        "Destino": "Recicladora Maomé Indústrias",
        "Status": "Disponível",

        "rota": [
            ("Condomínio São Paulo", "250 kg Papelão"),
            ("Edifício Itália", "200 kg Alumínio")
        ]
    }
]


# =========================================================
# ESTADO
# =========================================================

if "corridas" not in st.session_state:
    st.session_state["corridas"] = corridas.copy()


if "corrida_selecionada" not in st.session_state:
    st.session_state["corrida_selecionada"] = None


# =========================================================
# CARDS
# =========================================================

for corrida in st.session_state["corridas"]:

    if corrida["Status"] != "Disponível":
        continue

    with st.container(border=True):

        col1, col2, col3 = st.columns([2, 2, 1])

        # -------------------------------------------------
        # INFORMAÇÕES PRINCIPAIS
        # -------------------------------------------------

        with col1:

            st.subheader(
                f"🚚 Corrida #{corrida['ID']}"
            )

            st.write(
                f"🕐 **{corrida['Inicio']} → "
                f"{corrida['Fim']}**"
            )

            st.write(
                f"📍 **{corrida['Paradas']} paradas**"
            )

            st.write(
                f"⚖️ **{corrida['Peso']} kg**"
            )

        # -------------------------------------------------
        # PAGAMENTO
        # -------------------------------------------------

        with col2:

            st.metric(
                "Você recebe",
                f"R$ {corrida['Pagamento']:,.2f}"
            )

            st.write(
                f"Destino: **{corrida['Destino']}**"
            )

        # -------------------------------------------------
        # BOTÃO
        # -------------------------------------------------

        with col3:

            st.write("")

            if st.button(
                "Ver corrida",
                key=f"ver_{corrida['ID']}",
                use_container_width=True
            ):

                st.session_state[
                    "corrida_selecionada"
                ] = corrida["ID"]

                st.rerun()


# =========================================================
# DETALHAMENTO DA CORRIDA
# =========================================================

if st.session_state["corrida_selecionada"]:

    corrida_id = st.session_state["corrida_selecionada"]

    corrida = next(
        c for c in st.session_state["corridas"]
        if c["ID"] == corrida_id
    )

    st.divider()

    st.header(
        f"🚚 Corrida #{corrida['ID']}"
    )


    # =====================================================
    # RESUMO
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Início",
        corrida["Inicio"]
    )

    col2.metric(
        "Término",
        corrida["Fim"]
    )

    col3.metric(
        "Peso total",
        f"{corrida['Peso']} kg"
    )

    col4.metric(
        "Pagamento",
        f"R$ {corrida['Pagamento']:,.2f}"
    )


    st.divider()


    # =====================================================
    # ROTA
    # =====================================================

    st.subheader("🗺️ Fluxo da corrida")

    # Criar nós do Mermaid

    letras = [
        "A", "B", "C", "D", "E", "F", "G"
    ]

    nodes = []

    # Primeiro ponto
    primeiro_local = corrida["rota"][0][0]

    nodes.append(
        f'A["🏠 {primeiro_local}"]'
    )

    # Demais pontos
    for i, (local, material) in enumerate(
        corrida["rota"]
    ):

        letra = letras[i + 1]

        nodes.append(
            f'{letra}["{local}<br>{material}"]'
        )

    # Destino
    destino_letra = letras[
        len(corrida["rota"]) + 1
    ]

    nodes.append(
        f'{destino_letra}["♻️ {corrida["Destino"]}"]'
    )


    # Criar conexões
    connections = []

    for i in range(
        len(nodes) - 1
    ):

        connections.append(
            f"{letras[i]} --> {letras[i + 1]}"
        )


    mermaid = f"""
    graph LR

        {"".join(nodes)}

        {" ".join(connections)}

        style {destino_letra} fill:#4CAF50,stroke:#2E7D32,color:white
    """


    st_mermaid(mermaid)


    # =====================================================
    # PARADAS
    # =====================================================

    st.subheader("📦 Paradas")

    for i, (local, material) in enumerate(
        corrida["rota"],
        start=1
    ):

        with st.container(border=True):

            col1, col2 = st.columns([1, 4])

            with col1:

                st.metric(
                    "Parada",
                    i
                )

            with col2:

                st.write(
                    f"**{local}**"
                )

                st.write(
                    f"{material}"
                )


    # =====================================================
    # ACEITAR CORRIDA
    # =====================================================

    st.divider()

    st.warning(
        "Ao aceitar, você se compromete a realizar "
        f"a corrida entre {corrida['Inicio']} e "
        f"{corrida['Fim']}."
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "✅ Aceitar corrida",
            type="primary",
            use_container_width=True
        ):

            for c in st.session_state["corridas"]:

                if c["ID"] == corrida_id:

                    c["Status"] = "Aceita"

            st.success(
                "Corrida aceita com sucesso!"
            )

            st.session_state[
                "corrida_selecionada"
            ] = None

            st.rerun()


    with col2:

        if st.button(
            "Voltar",
            use_container_width=True
        ):

            st.session_state[
                "corrida_selecionada"
            ] = None

            st.rerun()
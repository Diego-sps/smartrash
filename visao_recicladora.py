import streamlit as st
import pandas as pd


# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.title("♻️ Recicladora Ousadia e Alegria")

st.subheader("Propostas recebidas")


# =========================================================
# PROPOSTAS SIMULADAS
# =========================================================

propostas = pd.DataFrame({
    "ID": ["P001", "P002", "P003"],
    "Gerador": [
        "Edifício Piazza São Pietro",
        "Vila Borguese",
        "Edifício Honduras"
    ],
    "Material": [
        "Alumínio",
        "Papelão",
        "Alumínio"
    ],
    "Quantidade": [
        100,
        300,
        200
    ],
    "Preço/kg": [
        3.50,
        1.00,
        3.90
    ],
    "Status": [
        "Pendente",
        "Pendente",
        "Pendente"
    ]
})


# =========================================================
# INICIALIZAÇÃO DO ESTADO
# =========================================================

if "propostas" not in st.session_state:
    st.session_state["propostas"] = propostas.copy()


if "proposta_selecionada" not in st.session_state:
    st.session_state["proposta_selecionada"] = None


# =========================================================
# LISTA DE PROPOSTAS
# =========================================================

df = st.session_state["propostas"]


for _, proposta in df.iterrows():

    if proposta["Status"] != "Pendente":
        continue

    valor_total = (
        proposta["Quantidade"] *
        proposta["Preço/kg"]
    )

    with st.container(border=True):

        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:

            st.subheader(
                proposta["Gerador"]
            )

            st.write(
                f"**Material:** {proposta['Material']}"
            )

            st.write(
                f"**Quantidade:** "
                f"{proposta['Quantidade']} kg"
            )

        with col2:

            st.metric(
                "Preço oferecido",
                f"R$ {proposta['Preço/kg']:.2f}/kg"
            )

            st.metric(
                "Valor total",
                f"R$ {valor_total:,.2f}"
            )

        with col3:

            if st.button(
                "Abrir",
                key=f"abrir_{proposta['ID']}"
            ):

                st.session_state[
                    "proposta_selecionada"
                ] = proposta["ID"]

                st.rerun()


# =========================================================
# DETALHAMENTO DA PROPOSTA
# =========================================================

if st.session_state["proposta_selecionada"]:

    proposta_id = (
        st.session_state["proposta_selecionada"]
    )

    proposta = df[
        df["ID"] == proposta_id
    ].iloc[0]

    st.divider()

    st.header(
        f"Proposta #{proposta['ID']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Gerador:** {proposta['Gerador']}"
        )

        st.write(
            f"**Material:** {proposta['Material']}"
        )

        st.write(
            f"**Quantidade:** "
            f"{proposta['Quantidade']} kg"
        )

    with col2:

        st.write(
            f"**Preço:** "
            f"R$ {proposta['Preço/kg']:.2f}/kg"
        )

        valor_total = (
            proposta["Quantidade"] *
            proposta["Preço/kg"]
        )

        st.write(
            f"**Valor total:** "
            f"R$ {valor_total:,.2f}"
        )

    st.divider()

    st.write(
        "Deseja aceitar esta proposta?"
    )

    col1, col2 = st.columns(2)

    # =====================================================
    # RECUSAR
    # =====================================================

    with col1:

        if st.button(
            "❌ Recusar proposta",
            use_container_width=True
        ):

            st.session_state["propostas"].loc[
                st.session_state["propostas"]["ID"] == proposta_id,
                "Status"
            ] = "Recusada"

            st.session_state[
                "proposta_selecionada"
            ] = None

            st.success(
                "Proposta recusada."
            )

            st.rerun()


    # =====================================================
    # ACEITAR
    # =====================================================

    with col2:

        if st.button(
            "✅ Aceitar proposta",
            type="primary",
            use_container_width=True
        ):

            st.session_state[
                "proposta_aceita"
            ] = proposta_id

            st.rerun()


# =========================================================
# DEFINIÇÃO DA LOGÍSTICA
# =========================================================

if "proposta_aceita" in st.session_state:

    proposta_id = (
        st.session_state["proposta_aceita"]
    )

    proposta = df[
        df["ID"] == proposta_id
    ].iloc[0]

    st.divider()

    st.header("🚚 Como deseja realizar a coleta?")

    st.write(
        f"Pedido #{proposta_id} — "
        f"{proposta['Quantidade']} kg de "
        f"{proposta['Material']}"
    )

    opcao = st.radio(
        "Escolha uma opção:",
        [
            "Vou buscar o pedido",
            "Vou contratar um transportador",
            "Deixar o SmarTrash encontrar o melhor transportador"
        ]
    )


    # =====================================================
    # OPÇÃO 1
    # =====================================================

    if opcao == "Vou buscar o pedido":

        st.info(
            "A recicladora será responsável "
            "pela coleta."
        )

        if st.button(
            "Confirmar coleta própria",
            type="primary"
        ):

            st.session_state["propostas"].loc[
                st.session_state["propostas"]["ID"] == proposta_id,
                "Status"
            ] = "Aceita"

            st.session_state[
                "logistica"
            ] = "Coleta própria"

            del st.session_state["proposta_aceita"]

            st.success(
                "Pedido aceito! "
                "A coleta será realizada pela recicladora."
            )

            st.rerun()


    # =====================================================
    # OPÇÃO 2
    # =====================================================

    elif opcao == "Vou contratar um transportador":

        st.info(
            "Você poderá selecionar uma transportadora "
            "cadastrada na plataforma."
        )

        transportador = st.selectbox(
            "Transportador",
            [
                "Roberto Transportes",
                "Claudio Logistics",
                "EcoLog Transportes"
            ]
        )

        if st.button(
            "Confirmar transportador",
            type="primary"
        ):

            st.session_state["propostas"].loc[
                st.session_state["propostas"]["ID"] == proposta_id,
                "Status"
            ] = "Aceita"

            st.session_state[
                "logistica"
            ] = transportador

            del st.session_state["proposta_aceita"]

            st.success(
                f"Pedido aceito! "
                f"Coleta delegada para {transportador}."
            )

            st.rerun()


    # =====================================================
    # OPÇÃO 3
    # =====================================================

    else:

        st.info(
            "O SmarTrash buscará o melhor transportador "
            "disponível considerando distância, capacidade, "
            "horário e custo."
        )

        if st.button(
            "🚀 Encontrar melhor transportador",
            type="primary"
        ):

            # FUTURO:
            # algoritmo de matching / otimização

            transportador_escolhido = (
                "Claudio Logistics"
            )

            st.session_state["propostas"].loc[
                st.session_state["propostas"]["ID"] == proposta_id,
                "Status"
            ] = "Aceita"

            st.session_state[
                "logistica"
            ] = transportador_escolhido

            del st.session_state["proposta_aceita"]

            st.success(
                f"Pedido aceito! "
                f"O SmarTrash selecionou: "
                f"{transportador_escolhido}"
            )

            st.rerun()
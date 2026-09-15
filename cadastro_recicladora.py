import streamlit as st
import pandas as pd

st.title("♻️ Marketplace")
st.subheader("Encontre a melhor recicladora para os seus resíduos")

# ---------------------------------------------------------
# DADOS SIMULADOS DAS RECICLADORAS
# ---------------------------------------------------------

recicladoras = [
    {
        "Nome": "Recicladora Ousadia e Alegria",
        "Endereço": "Rua Marina Crespi, 118",
        "Aluminio": 3.50,
        "Papelão": 0.42,
        "Plastico": 1.20,
    },
    {
        "Nome": "Recicladora Maomé Indústrias",
        "Endereço": "Rua Marques de Valença, 398",
        "Aluminio": 3.90,
        "Papelão": 1.00,
        "Plastico": 1.50,
    },
    {
        "Nome": "Recicla Mooca",
        "Endereço": "Rua da Mooca, 850",
        "Aluminio": 3.70,
        "Papelão": 0.75,
        "Plastico": 1.10,
    },
]

df_recicladoras = pd.DataFrame(recicladoras)


# ---------------------------------------------------------
# RESÍDUOS DO GERADOR
# ---------------------------------------------------------

st.header("Seus resíduos")

col1, col2, col3 = st.columns(3)

with col1:
    aluminio = st.number_input(
        "Alumínio (kg)",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

with col2:
    papelao = st.number_input(
        "Papelão (kg)",
        min_value=0.0,
        value=300.0,
        step=10.0
    )

with col3:
    plastico = st.number_input(
        "Plástico (kg)",
        min_value=0.0,
        value=200.0,
        step=10.0
    )


st.divider()

# ---------------------------------------------------------
# FILTRO
# ---------------------------------------------------------

st.header("Recicladoras disponíveis")

material_filtro = st.selectbox(
    "Filtrar por material",
    ["Todos", "Alumínio", "Papelão", "Plástico"]
)


# ---------------------------------------------------------
# CARDS
# ---------------------------------------------------------

for _, recicladora in df_recicladoras.iterrows():

    if material_filtro == "Alumínio":
        preco = recicladora["Aluminio"]
        material = "Alumínio"
        quantidade = aluminio

    elif material_filtro == "Papelão":
        preco = recicladora["Papelão"]
        material = "Papelão"
        quantidade = papelao

    elif material_filtro == "Plástico":
        preco = recicladora["Plastico"]
        material = "Plástico"
        quantidade = plastico

    else:
        preco = None
        material = None
        quantidade = 0


    # -----------------------------------------------------
    # CARD
    # -----------------------------------------------------

    with st.container(border=True):

        col1, col2 = st.columns([3, 1])

        with col1:

            st.subheader(recicladora["Nome"])

            st.write(
                f"📍 {recicladora['Endereço']}"
            )

            st.write("**Preços oferecidos:**")

            preco_col1, preco_col2, preco_col3 = st.columns(3)

            with preco_col1:
                st.metric(
                    "Alumínio",
                    f"R$ {recicladora['Aluminio']:.2f}/kg"
                )

            with preco_col2:
                st.metric(
                    "Papelão",
                    f"R$ {recicladora['Papelão']:.2f}/kg"
                )

            with preco_col3:
                st.metric(
                    "Plástico",
                    f"R$ {recicladora['Plastico']:.2f}/kg"
                )

        with col2:

            st.write("")

            if material_filtro != "Todos":

                valor = quantidade * preco

                st.write(
                    f"**Sua quantidade:**  \n"
                    f"{quantidade:.0f} kg"
                )

                st.write(
                    f"**Valor estimado:**  \n"
                    f"R$ {valor:,.2f}"
                )

            if st.button(
                "Fazer proposta",
                key=f"proposta_{recicladora['Nome']}"
            ):

                st.session_state["recicladora_selecionada"] = (
                    recicladora["Nome"]
                )

                st.session_state["proposta_aberta"] = True


# ---------------------------------------------------------
# MODAL / FORMULÁRIO DE PROPOSTA
# ---------------------------------------------------------

if st.session_state.get("proposta_aberta", False):

    nome_recicladora = st.session_state["recicladora_selecionada"]

    recicladora = df_recicladoras[
        df_recicladoras["Nome"] == nome_recicladora
    ].iloc[0]

    st.divider()

    st.header("📨 Enviar proposta")

    st.write(
        f"Você está fazendo uma proposta para "
        f"**{nome_recicladora}**."
    )

    material = st.selectbox(
        "Material",
        ["Alumínio", "Papelão", "Plástico"]
    )

    if material == "Alumínio":
        preco = recicladora["Aluminio"]
        quantidade_padrao = aluminio

    elif material == "Papelão":
        preco = recicladora["Papelão"]
        quantidade_padrao = papelao

    else:
        preco = recicladora["Plastico"]
        quantidade_padrao = plastico


    quantidade = st.number_input(
        "Quantidade (kg)",
        min_value=1.0,
        value=float(quantidade_padrao),
        step=10.0
    )

    valor_total = quantidade * preco

    st.info(
        f"Preço oferecido: **R$ {preco:.2f}/kg**\n\n"
        f"Valor estimado da proposta: **R$ {valor_total:,.2f}**"
    )


    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Enviar proposta",
            type="primary"
        ):

            # Aqui futuramente salvaremos no banco

            nova_proposta = {
                "Recicladora": nome_recicladora,
                "Material": material,
                "Quantidade": quantidade,
                "Preço/kg": preco,
                "Valor Total": valor_total,
                "Status": "Pendente"
            }

            st.session_state["ultima_proposta"] = nova_proposta
            st.session_state["proposta_aberta"] = False

            st.success(
                "Proposta enviada com sucesso!"
            )

    with col2:

        if st.button("Cancelar"):

            st.session_state["proposta_aberta"] = False
            st.rerun()


# ---------------------------------------------------------
# ÚLTIMA PROPOSTA
# ---------------------------------------------------------

if "ultima_proposta" in st.session_state:

    proposta = st.session_state["ultima_proposta"]

    st.divider()

    st.header("📋 Minha última proposta")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Recicladora",
        proposta["Recicladora"]
    )

    col2.metric(
        "Material",
        proposta["Material"]
    )

    col3.metric(
        "Quantidade",
        f"{proposta['Quantidade']:.0f} kg"
    )

    col4.metric(
        "Status",
        proposta["Status"]
    )
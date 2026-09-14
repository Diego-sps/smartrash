import streamlit as st

cadastro_gerador = st.Page("cadastro_recicladora.py", title="Cadastrar Gerador", icon=":material/add_circle:")
visao_recicladora = st.Page("visao_recicladora.py", title="Visão Reciclador", icon=":material/delete:")
dashboard_mensal = st.Page("dashboard_mensal.py", title="Dashboard Mensal", icon=":material/bar_chart:")

pg = st.navigation([cadastro_gerador, visao_recicladora, dashboard_mensal])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
import streamlit as st

cadastro_gerador = st.Page("cadastro_recicladora.py", title="Cadastrar Gerador", icon=":material/add_circle:")
visao_recicladora = st.Page("visao_recicladora.py", title="Visão Reciclador", icon=":material/delete:")
dashboard_mensal = st.Page("dashboard_mensal.py", title="Visão recicladora Pedidos Aceitos", icon=":material/bar_chart:")
visao_pedidos_gerador = st.Page("visao_pedidos_gerador.py", title="Visão Pedidos Gerador", icon=":material/bar_chart:")
visao_coletor = st.Page("visao_coletor.py", title="Visão Coletor", icon=":material/bar_chart:")


pg = st.navigation([cadastro_gerador, visao_recicladora, dashboard_mensal, visao_pedidos_gerador, visao_coletor])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
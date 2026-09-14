import streamlit as st
import pandas as pd


def cadastrar_gerador(nom, cnpj, address, tel, email, responsavel, horario_funcionamento, tipo_material, preco_estimado):
    df_banco = pd.read_excel("teste_banco_recicladoras.xlsx")
    df_banco = pd.concat([df_banco, pd.DataFrame({"Nome": [nom], "CNPJ": [cnpj], "Endereço": [address], "Telefone": [tel], "Email": [email], "Responsável": [responsavel], "Horário de Funcionamento": [horario_funcionamento], "Tipo de Material Aceito": [tipo_material], "Preço Estimado Material": [preco_estimado]})], ignore_index=True)
    df_banco.to_excel("teste_banco_recicladoras.xlsx", index=False)
    st.success("Gerador cadastrado com sucesso!")


st.write("Cadastro de Gerador")
nom = st.text_input("Nome do Gerador",key="nome_gerador")
cnpj = st.text_input("CNPJ",key="cnpj")
address =st.text_input("Endereço",key="address")
tel = st.text_input("Telefone",key="tel")
email = st.text_input("Email",key="email")
responsavel = st.text_input("Responsável",key="responsavel")
horario_funcionamento = st.text_input("Horário de Funcionamento",key="horario_funcionamento")
tipo_material = st.text_input("Tipo de Material Aceito",key="tipo_material")
preco_estimado = st.text_input("Preço Estimado Material",key="preco_estimado")
st.button("Cadastrar", on_click=cadastrar_gerador, args=(nom, cnpj, address, tel, email, responsavel, horario_funcionamento, tipo_material, preco_estimado))
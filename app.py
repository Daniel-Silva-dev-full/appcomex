import streamlit as st
import pandas as pd
import locale
import altair as alt

# Ler dados de exportação
df_exp = pd.read_csv('EXP_2023.csv',sep=';',encoding='latin1')

#ler dados da tabela de pais
df_pais = pd.read_csv('PAIS.csv',sep=';',encoding='latin1')

# Mesclar os DataFrames 
df_merg = pd.merge(df_exp, df_pais, on='CO_PAIS', how='inner')

df_final = df_merg.drop(['CO_UNID', 'CO_PAIS', 'CO_VIA', 'CO_PAIS_ISON3', 'CO_PAIS_ISOA3', 'NO_PAIS_ING','NO_PAIS_ESP'], axis=1)


# Definir o locale para Português
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Calcular as somas
vlr_kg = df_final['KG_LIQUIDO'].sum() / 1000000  # Dividindo por 1 milhão
vlr_exp = df_final['VL_FOB'].sum() / 1000000  # Dividindo por 1 milhão
qtd_prod = df_final['CO_NCM'].count()/ 1000000

# Formatando
vlr_exp_mm = locale.currency(vlr_kg, grouping=True, symbol=None)
vlr_fob_mm = locale.currency(vlr_exp, grouping=True, symbol=None)

# Configuração da páginaso streamlit

st.set_page_config(
    page_icon="🏨",
    layout='wide',  
    initial_sidebar_state='expanded',
)

st.write("Desenvolvido Por Daniel Pereira da Silva")
st.title("Análise de Exportação Estados 2023")

# Adicionar espaço
st.markdown("---")
st.subheader("Indicadores de Desempenho")

# Adicionar os filtros
with st.sidebar:
    st.write("Use os filtros para analisar os dados.")
    # Filtrar por NO_PAIS
    paises_selecionados = st.multiselect('Selecione os países', df_final['NO_PAIS'].unique())
    
    # Filtrar por SG_UF_NCM
    ufs_selecionados = st.multiselect('Selecione os estados', df_final['SG_UF_NCM'].unique())


# Aplicar filtros
if paises_selecionados or ufs_selecionados:
    df_filtrado = df_final.query('NO_PAIS in @paises_selecionados or SG_UF_NCM in @ufs_selecionados')
else:
    df_filtrado = df_final.copy()  

# Calcular as somas das colunas
vlr_kg = df_filtrado['KG_LIQUIDO'].sum() / 1000000  # Dividindo por 1 milhão
vlr_exp = df_filtrado['VL_FOB'].sum() / 1000000  # Dividindo por 1 milhão
qtd_prod = df_filtrado['CO_NCM'].count()

# Adicionar separador
qtd_prod_formatada = '{:,}'.format(qtd_prod)

# Formatando 
vlr_exp_mm = locale.currency(vlr_kg, grouping=True, symbol=None)
vlr_fob_mm = locale.currency(vlr_exp, grouping=True, symbol=None)

# Exibir os cards
col1, col2, col3 = st.columns(3)
col1.metric("Valor FOB (MM)", vlr_fob_mm)
col2.metric("Qtd Kg Liquido(MM)", vlr_exp_mm)
col3.metric("Qtde Produtos Exportados", qtd_prod_formatada)


st.markdown("---")


uf_maior_faturamento = df_filtrado.groupby('SG_UF_NCM')['VL_FOB'].sum().idxmax()
mes_maior_faturamento = df_filtrado.groupby('CO_MES')['VL_FOB'].sum().idxmax()

st.subheader("Indicadores de Destaque")
st.info(f"**Estado com maior Valor de Exportação:** {uf_maior_faturamento}")
st.info(f"**Mês com maior Valor de Exportação:** {mes_maior_faturamento} / 2023")


st.markdown("---")

# Agrupar os dados por mês
st.subheader("Exportações por Mês")
df_agrupado = df_filtrado.groupby('CO_MES')['VL_FOB'].sum().reset_index()
st.bar_chart(df_agrupado.set_index('CO_MES'),color="#4ECAF2")


st.markdown("---")
st.subheader("Exportações por Estados")
df_agrupado_uf = df_filtrado.groupby('SG_UF_NCM')['VL_FOB'].sum().reset_index()
st.bar_chart(df_agrupado_uf.set_index('SG_UF_NCM'),color="#4E8FF2")


st.markdown("---")

st.subheader("Faça o download do arquivo abaixo")
# Botão para fazer o download do arquivo CSV
st.download_button(label="Download CSV", data=df_filtrado.to_csv(index=False, encoding='utf-8-sig'), file_name='comex.csv', mime='text/csv')



# app.py
"""Aplicação principal - Conversor NF-e"""

import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Imports dos módulos personalizados
from config import PAGE_CONFIG, CAMPOS_DISPONIVEIS, CAMPOS_PRODUTOS, CAMPOS_PADRAO_NOTAS, CAMPOS_PADRAO_PRODUTOS
from styles import get_custom_css, get_header_html, get_info_cards_html, get_metric_card_html, get_footer_html
from file_processor import FileProcessor
from excel_generator import ExcelGenerator

# Configuração da página
st.set_page_config(**PAGE_CONFIG)

# Aplica CSS customizado
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ========== UPLOAD DE LOGO (SIDEBAR) ==========
with st.sidebar:
    st.markdown("### 🖼️ Personalizar Logo")
    logo_file = st.file_uploader(
        "Envie o logo da empresa",
        type=['png', 'jpg', 'jpeg'],
        help="Imagem que aparecerá no cabeçalho (recomendado: quadrada, 500x500px)"
    )
    
    logo_base64 = None
    if logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Sobre a Aplicação
    
    **✅ Formatos Aceitos:**
    - Arquivo ZIP com múltiplos XMLs
    - Arquivos XML individuais
    - Padrão NF-e nacional
    
    **📊 Funcionalidades:**
    - Seleção personalizada de campos
    - Formatação automática de dados
    - Exportação para Excel organizado
    - Resumos estatísticos
    """)

# Header personalizado com logo
st.markdown(get_header_html(logo_base64), unsafe_allow_html=True)

# Conteúdo principal - Cards informativos
col1, col2, col3 = st.columns(3)
cards = get_info_cards_html()

with col1:
    st.markdown(cards[0], unsafe_allow_html=True)
with col2:
    st.markdown(cards[1], unsafe_allow_html=True)
with col3:
    st.markdown(cards[2], unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========== CONFIGURAÇÕES NA TELA PRINCIPAL ==========
st.markdown("---")
st.markdown("## ⚙️ Configurações")

col1, col2 = st.columns(2)

with col1:
    formatar_dados = st.checkbox(
        "✅ Formatar dados automaticamente", 
        value=True,
        help="Aplica formatação brasileira: moeda (R$ 1.234,56), data (DD/MM/AAAA), CNPJ/CPF"
    )

with col2:
    incluir_resumo = st.checkbox(
        "✅ Incluir aba de resumo estatístico", 
        value=True,
        help="Adiciona uma aba com totalizadores e estatísticas no Excel"
    )

st.markdown("---")

# ========== SELEÇÃO DE CAMPOS NA TELA PRINCIPAL ==========
st.markdown("## 🔧 Campos das Notas Fiscais")
st.markdown("*Selecione os campos que deseja extrair das notas fiscais:*")

# Inicializa estado se não existir
if 'campos_selecionados_notas' not in st.session_state:
    st.session_state.campos_selecionados_notas = CAMPOS_PADRAO_NOTAS.copy()

# Cria colunas para os expanders
col1, col2 = st.columns(2)

campos_selecionados_notas = []
categorias = list(CAMPOS_DISPONIVEIS.items())

# Primeira coluna - Dados da Nota e Emitente
with col1:
    for categoria, campos in categorias[:2]:
        with st.expander(f"📁 {categoria}", expanded=(categoria == "Dados da Nota")):
            for campo_id, config in campos.items():
                is_checked = campo_id in st.session_state.campos_selecionados_notas
                if st.checkbox(config['label'], value=is_checked, key=f"nota_{campo_id}"):
                    campos_selecionados_notas.append(campo_id)

# Segunda coluna - Destinatário e Valores
with col2:
    for categoria, campos in categorias[2:]:
        with st.expander(f"📁 {categoria}", expanded=(categoria == "Valores")):
            for campo_id, config in campos.items():
                is_checked = campo_id in st.session_state.campos_selecionados_notas
                if st.checkbox(config['label'], value=is_checked, key=f"nota_{campo_id}"):
                    campos_selecionados_notas.append(campo_id)

st.session_state.campos_selecionados_notas = campos_selecionados_notas

st.markdown("<br>", unsafe_allow_html=True)

# Seleção de campos para produtos
st.markdown("## 📦 Campos dos Produtos")
st.markdown("*Selecione os campos que deseja extrair dos produtos:*")

if 'campos_selecionados_produtos' not in st.session_state:
    st.session_state.campos_selecionados_produtos = CAMPOS_PADRAO_PRODUTOS.copy()

campos_selecionados_produtos = []

# Divide produtos em 2 colunas
campos_produtos_list = list(CAMPOS_PRODUTOS.items())
metade = len(campos_produtos_list) // 2

col1, col2 = st.columns(2)

with col1:
    with st.expander("📦 Campos Disponíveis - Parte 1", expanded=True):
        for campo_id, config in campos_produtos_list[:metade]:
            is_checked = campo_id in st.session_state.campos_selecionados_produtos
            if st.checkbox(config['label'], value=is_checked, key=f"prod_{campo_id}"):
                campos_selecionados_produtos.append(campo_id)

with col2:
    with st.expander("📦 Campos Disponíveis - Parte 2", expanded=True):
        for campo_id, config in campos_produtos_list[metade:]:
            is_checked = campo_id in st.session_state.campos_selecionados_produtos
            if st.checkbox(config['label'], value=is_checked, key=f"prod_{campo_id}"):
                campos_selecionados_produtos.append(campo_id)

st.session_state.campos_selecionados_produtos = campos_selecionados_produtos

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# Validação de campos selecionados
if not st.session_state.campos_selecionados_notas:
    st.warning("⚠️ Selecione pelo menos um campo das Notas Fiscais para continuar!")
    st.stop()

# ========== UPLOAD DE ARQUIVOS ==========
st.markdown("## 📤 Upload de Arquivos")

# Opções de upload
upload_option = st.radio(
    "Escolha o método de envio:",
    ["🗜️ Arquivo ZIP (múltiplos XMLs)", "📄 Arquivos XML individuais"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Processamento baseado na opção escolhida
if "🗜️" in upload_option:
    uploaded_zip = st.file_uploader(
        "Envie um arquivo ZIP contendo os XMLs das notas fiscais",
        type=['zip'],
        help="Selecione um arquivo ZIP que contenha os XMLs"
    )
    
    if uploaded_zip:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 PROCESSAR ARQUIVOS", use_container_width=True):
                with st.spinner("⚙️ Processando arquivos..."):
                    # Cria processador com campos selecionados
                    processor = FileProcessor(
                        st.session_state.campos_selecionados_notas,
                        st.session_state.campos_selecionados_produtos,
                        formatar_dados
                    )
                    
                    notas_data, produtos_data = processor.processar_zip(uploaded_zip)
                    
                    if notas_data:
                        df_notas = pd.DataFrame(notas_data)
                        df_produtos = pd.DataFrame(produtos_data)
                        
                        st.success("✅ Processamento concluído com sucesso!")
                        
                        # Exibe métricas
                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(get_metric_card_html(len(df_notas), "Notas Fiscais"), unsafe_allow_html=True)
                        with col2:
                            st.markdown(get_metric_card_html(len(df_produtos), "Produtos"), unsafe_allow_html=True)
                        with col3:
                            if 'Valor Total' in df_notas.columns:
                                if formatar_dados:
                                    valores = df_notas['Valor Total'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.')
                                    total = valores.astype(float).sum()
                                    valor_formatado = f"R$ {total:,.0f}".replace(',', '.')
                                else:
                                    total = df_notas['Valor Total'].astype(float).sum()
                                    valor_formatado = f"R$ {total:,.0f}"
                                st.markdown(get_metric_card_html(valor_formatado, "Valor Total"), unsafe_allow_html=True)
                            else:
                                st.markdown(get_metric_card_html("-", "Valor Total"), unsafe_allow_html=True)
                        with col4:
                            if 'Valor Total' in df_notas.columns:
                                if formatar_dados:
                                    valores = df_notas['Valor Total'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.')
                                    media = valores.astype(float).mean()
                                    valor_formatado = f"R$ {media:,.0f}".replace(',', '.')
                                else:
                                    media = df_notas['Valor Total'].astype(float).mean()
                                    valor_formatado = f"R$ {media:,.0f}"
                                st.markdown(get_metric_card_html(valor_formatado, "Valor Médio"), unsafe_allow_html=True)
                            else:
                                st.markdown(get_metric_card_html("-", "Valor Médio"), unsafe_allow_html=True)
                        
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        
                        # Preview dos dados
                        tab1, tab2 = st.tabs(["📋 Notas Fiscais", "📦 Produtos"])
                        
                        with tab1:
                            st.dataframe(df_notas, use_container_width=True, height=400)
                        
                        with tab2:
                            if not df_produtos.empty:
                                st.dataframe(df_produtos, use_container_width=True, height=400)
                            else:
                                st.info("Nenhum campo de produto foi selecionado.")
                        
                        # Gera arquivo Excel
                        excel_gen = ExcelGenerator()
                        excel_file = excel_gen.criar_excel(df_notas, df_produtos, incluir_resumo)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="📥 BAIXAR PLANILHA EXCEL",
                                data=excel_file,
                                file_name=f"TRR_Notas_Fiscais_{timestamp}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ Nenhum dado foi extraído dos arquivos XML.")

else:
    uploaded_files = st.file_uploader(
        "Envie os arquivos XML das notas fiscais",
        type=['xml'],
        accept_multiple_files=True,
        help="Selecione um ou mais arquivos XML"
    )
    
    if uploaded_files:
        st.info(f"📊 **{len(uploaded_files)}** arquivo(s) selecionado(s)")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 PROCESSAR ARQUIVOS", use_container_width=True):
                with st.spinner("⚙️ Processando arquivos..."):
                    processor = FileProcessor(
                        st.session_state.campos_selecionados_notas,
                        st.session_state.campos_selecionados_produtos,
                        formatar_dados
                    )
                    
                    notas_data, produtos_data = processor.processar_arquivos_individuais(uploaded_files)
                    
                    if notas_data:
                        df_notas = pd.DataFrame(notas_data)
                        df_produtos = pd.DataFrame(produtos_data)
                        
                        st.success("✅ Processamento concluído com sucesso!")
                        
                        # Métricas
                        st.markdown("<br>", unsafe_allow_html=True)
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(get_metric_card_html(len(df_notas), "Notas Fiscais"), unsafe_allow_html=True)
                        with col2:
                            st.markdown(get_metric_card_html(len(df_produtos), "Produtos"), unsafe_allow_html=True)
                        with col3:
                            if 'Valor Total' in df_notas.columns:
                                if formatar_dados:
                                    valores = df_notas['Valor Total'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.')
                                    total = valores.astype(float).sum()
                                    valor_formatado = f"R$ {total:,.0f}".replace(',', '.')
                                else:
                                    total = df_notas['Valor Total'].astype(float).sum()
                                    valor_formatado = f"R$ {total:,.0f}"
                                st.markdown(get_metric_card_html(valor_formatado, "Valor Total"), unsafe_allow_html=True)
                            else:
                                st.markdown(get_metric_card_html("-", "Valor Total"), unsafe_allow_html=True)
                        with col4:
                            if 'Valor Total' in df_notas.columns:
                                if formatar_dados:
                                    valores = df_notas['Valor Total'].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.')
                                    media = valores.astype(float).mean()
                                    valor_formatado = f"R$ {media:,.0f}".replace(',', '.')
                                else:
                                    media = df_notas['Valor Total'].astype(float).mean()
                                    valor_formatado = f"R$ {media:,.0f}"
                                st.markdown(get_metric_card_html(valor_formatado, "Valor Médio"), unsafe_allow_html=True)
                            else:
                                st.markdown(get_metric_card_html("-", "Valor Médio"), unsafe_allow_html=True)
                        
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        
                        # Preview
                        tab1, tab2 = st.tabs(["📋 Notas Fiscais", "📦 Produtos"])
                        
                        with tab1:
                            st.dataframe(df_notas, use_container_width=True, height=400)
                        
                        with tab2:
                            if not df_produtos.empty:
                                st.dataframe(df_produtos, use_container_width=True, height=400)
                            else:
                                st.info("Nenhum campo de produto foi selecionado.")
                        
                        # Gera Excel
                        excel_gen = ExcelGenerator()
                        excel_file = excel_gen.criar_excel(df_notas, df_produtos, incluir_resumo)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="📥 BAIXAR PLANILHA EXCEL",
                                data=excel_file,
                                file_name=f"TRR_Notas_Fiscais_{timestamp}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ Nenhum dado foi extraído dos arquivos XML.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown(get_footer_html(), unsafe_allow_html=True)
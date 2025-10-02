# styles.py
"""Estilos CSS para a aplicação Streamlit"""

def get_custom_css():
    """Retorna o CSS personalizado da aplicação"""
    return """
    <style>
        /* Paleta de cores principal */
        :root {
            --primary-blue: #0000FF;
            --dark-blue: #0000CC;
            --light-blue: #E6E6FF;
            --white: #FFFFFF;
            --gray-100: #F8F9FA;
            --gray-200: #E9ECEF;
            --gray-800: #343A40;
        }
        
        /* Esconde elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Container principal */
        .main {
            background-color: #F8F9FA;
        }
        
        /* Header personalizado */
        .custom-header {
            background: linear-gradient(135deg, #0000FF 0%, #0000CC 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }
        
        .logo-circle {
            background-color: white;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }
        
        .logo-circle img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .custom-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .custom-header p {
            color: #E6E6FF;
            font-size: 1.1rem;
            margin-top: 0.5rem;
        }
        
        /* Cards informativos */
        .info-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #0000FF;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #0000FF 0%, #0000CC 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card h3 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
        
        .metric-card p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }
        
        /* Card de configurações */
        .config-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border: 2px solid #E6E6FF;
            margin-bottom: 1.5rem;
        }
        
        .config-card h3 {
            color: #0000CC;
            margin-top: 0;
            font-size: 1.3rem;
        }
        
        /* Botões personalizados */
        .stButton>button {
            background: linear-gradient(135deg, #0000FF 0%, #0000CC 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Upload area */
        .uploadedFile {
            border: 2px dashed #0000FF;
            border-radius: 10px;
            padding: 1rem;
            background-color: #E6E6FF;
        }
        
        /* Tabelas */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: white;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #E6E6FF;
            border-radius: 8px;
            font-weight: 600;
            color: #0000CC;
        }
        
        /* Selectbox customizado */
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #0000FF;
        }
        
        /* Checkbox customizado */
        .stCheckbox {
            padding: 0.3rem 0;
        }
    </style>
    """

def get_header_html(logo_base64=None):
    """Retorna o HTML do header personalizado"""
    if logo_base64:
        logo_content = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo"/>'
    else:
        logo_content = '<span style="color: #0000FF; font-size: 2rem; font-weight: 900;">TRR</span>'
    
    return f"""
    <div class="custom-header">
        <div class="logo-container">
            <div class="logo-circle">
                {logo_content}
            </div>
        </div>
        <h1>Conversor NF-e Profissional</h1>
        <p>Transforme XMLs de Notas Fiscais em Planilhas Excel Organizadas</p>
    </div>
    """

def get_info_cards_html():
    """Retorna HTML dos cards informativos"""
    return """
    <div class="info-card">
        <h3 style="color: #0000FF; margin: 0;">🚀 Rápido</h3>
        <p style="margin: 0.5rem 0 0 0; color: #666;">Processe centenas de XMLs em segundos</p>
    </div>
    """, """
    <div class="info-card">
        <h3 style="color: #0000FF; margin: 0;">🎯 Preciso</h3>
        <p style="margin: 0.5rem 0 0 0; color: #666;">Extração completa de todos os dados</p>
    </div>
    """, """
    <div class="info-card">
        <h3 style="color: #0000FF; margin: 0;">📊 Organizado</h3>
        <p style="margin: 0.5rem 0 0 0; color: #666;">Excel com abas separadas e resumos</p>
    </div>
    """

def get_metric_card_html(valor, label):
    """Retorna HTML de um card de métrica"""
    return f"""
    <div class="metric-card">
        <h3>{valor}</h3>
        <p>{label}</p>
    </div>
    """

def get_footer_html():
    """Retorna HTML do footer"""
    return """
    <div style="text-align: center; color: #666;">
        <p style="margin: 0;">Desenvolvido com ❤️ por <strong>TRR Contabilidade</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Powered by Python 🐍 & Streamlit</p>
    </div>
    """
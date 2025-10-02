# config.py
"""Configurações gerais da aplicação"""

# Configurações da página Streamlit
PAGE_CONFIG = {
    "page_title": "TRR - Conversor NF-e",
    "page_icon": "📄",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Paleta de cores
COLORS = {
    "primary_blue": "#0000FF",
    "dark_blue": "#0000CC",
    "light_blue": "#E6E6FF",
    "white": "#FFFFFF",
    "gray_100": "#F8F9FA",
    "gray_200": "#E9ECEF",
    "gray_800": "#343A40"
}

# Namespaces XML NF-e
XML_NAMESPACES = {
    'nfe': 'http://www.portalfiscal.inf.br/nfe'
}

# Mapeamento de campos disponíveis para extração
CAMPOS_DISPONIVEIS = {
    "Dados da Nota": {
        "numero_nf": {"label": "Número NF", "path": "ide/nNF", "tipo": "texto"},
        "serie": {"label": "Série", "path": "ide/serie", "tipo": "texto"},
        "data_emissao": {"label": "Data Emissão", "path": "ide/dhEmi", "tipo": "data"},
        "chave": {"label": "Chave de Acesso", "path": "@Id", "tipo": "texto"},
        "modelo": {"label": "Modelo", "path": "ide/mod", "tipo": "texto"},
        "natureza_operacao": {"label": "Natureza da Operação", "path": "ide/natOp", "tipo": "texto"},
    },
    "Emitente": {
        "emit_cnpj": {"label": "CNPJ Emitente", "path": "emit/CNPJ", "tipo": "cnpj"},
        "emit_nome": {"label": "Nome Emitente", "path": "emit/xNome", "tipo": "texto"},
        "emit_fantasia": {"label": "Nome Fantasia Emitente", "path": "emit/xFant", "tipo": "texto"},
        "emit_ie": {"label": "IE Emitente", "path": "emit/IE", "tipo": "texto"},
        "emit_uf": {"label": "UF Emitente", "path": "emit/enderEmit/UF", "tipo": "texto"},
        "emit_municipio": {"label": "Município Emitente", "path": "emit/enderEmit/xMun", "tipo": "texto"},
    },
    "Destinatário": {
        "dest_cnpj_cpf": {"label": "CNPJ/CPF Destinatário", "path": "dest/CNPJ|dest/CPF", "tipo": "cnpj_cpf"},
        "dest_nome": {"label": "Nome Destinatário", "path": "dest/xNome", "tipo": "texto"},
        "dest_ie": {"label": "IE Destinatário", "path": "dest/IE", "tipo": "texto"},
        "dest_uf": {"label": "UF Destinatário", "path": "dest/enderDest/UF", "tipo": "texto"},
        "dest_municipio": {"label": "Município Destinatário", "path": "dest/enderDest/xMun", "tipo": "texto"},
    },
    "Valores": {
        "valor_produtos": {"label": "Valor Produtos", "path": "total/ICMSTot/vProd", "tipo": "moeda"},
        "valor_frete": {"label": "Valor Frete", "path": "total/ICMSTot/vFrete", "tipo": "moeda"},
        "valor_seguro": {"label": "Valor Seguro", "path": "total/ICMSTot/vSeg", "tipo": "moeda"},
        "valor_desconto": {"label": "Valor Desconto", "path": "total/ICMSTot/vDesc", "tipo": "moeda"},
        "valor_icms": {"label": "Valor ICMS", "path": "total/ICMSTot/vICMS", "tipo": "moeda"},
        "valor_ipi": {"label": "Valor IPI", "path": "total/ICMSTot/vIPI", "tipo": "moeda"},
        "valor_pis": {"label": "Valor PIS", "path": "total/ICMSTot/vPIS", "tipo": "moeda"},
        "valor_cofins": {"label": "Valor COFINS", "path": "total/ICMSTot/vCOFINS", "tipo": "moeda"},
        "valor_total": {"label": "Valor Total", "path": "total/ICMSTot/vNF", "tipo": "moeda"},
    }
}

CAMPOS_PRODUTOS = {
    "codigo": {"label": "Código", "path": "prod/cProd", "tipo": "texto"},
    "descricao": {"label": "Descrição", "path": "prod/xProd", "tipo": "texto"},
    "ncm": {"label": "NCM", "path": "prod/NCM", "tipo": "texto"},
    "cfop": {"label": "CFOP", "path": "prod/CFOP", "tipo": "texto"},
    "unidade": {"label": "Unidade", "path": "prod/uCom", "tipo": "texto"},
    "quantidade": {"label": "Quantidade", "path": "prod/qCom", "tipo": "numero"},
    "valor_unitario": {"label": "Valor Unitário", "path": "prod/vUnCom", "tipo": "moeda"},
    "valor_total": {"label": "Valor Total", "path": "prod/vProd", "tipo": "moeda"},
    "ean": {"label": "EAN", "path": "prod/cEAN", "tipo": "texto"},
}

# Campos padrão selecionados
CAMPOS_PADRAO_NOTAS = [
    "numero_nf", "serie", "data_emissao", "chave",
    "emit_cnpj", "emit_nome", "emit_uf",
    "dest_cnpj_cpf", "dest_nome", "dest_uf",
    "valor_produtos", "valor_total"
]

CAMPOS_PADRAO_PRODUTOS = [
    "codigo", "descricao", "ncm", "cfop",
    "unidade", "quantidade", "valor_unitario", "valor_total"
]
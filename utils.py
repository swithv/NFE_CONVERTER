# utils.py
"""Funções utilitárias para formatação e manipulação de dados"""

from datetime import datetime
import re

def formatar_moeda(valor):
    """Formata valor numérico como moeda brasileira"""
    try:
        if valor == '' or valor is None:
            return 'R$ 0,00'
        valor_float = float(str(valor).replace(',', '.'))
        return f'R$ {valor_float:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
    except:
        return 'R$ 0,00'

def formatar_numero(valor, decimais=2):
    """Formata valor numérico com casas decimais"""
    try:
        if valor == '' or valor is None:
            return '0,00'
        valor_float = float(str(valor).replace(',', '.'))
        return f'{valor_float:.{decimais}f}'.replace('.', ',')
    except:
        return '0,00'

def formatar_data(data_str):
    """Formata data ISO para formato brasileiro"""
    try:
        if not data_str:
            return ''
        # Remove timezone se existir
        data_str = data_str.split('-03:00')[0].split('T')[0]
        if len(data_str) == 10:  # YYYY-MM-DD
            data = datetime.strptime(data_str, '%Y-%m-%d')
            return data.strftime('%d/%m/%Y')
        return data_str
    except:
        return data_str

def formatar_cnpj(cnpj):
    """Formata CNPJ com máscara"""
    try:
        cnpj = re.sub(r'\D', '', str(cnpj))
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj
    except:
        return cnpj

def formatar_cpf(cpf):
    """Formata CPF com máscara"""
    try:
        cpf = re.sub(r'\D', '', str(cpf))
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf
    except:
        return cpf

def formatar_cnpj_cpf(documento):
    """Identifica e formata CNPJ ou CPF"""
    documento = re.sub(r'\D', '', str(documento))
    if len(documento) == 14:
        return formatar_cnpj(documento)
    elif len(documento) == 11:
        return formatar_cpf(documento)
    return documento

def aplicar_formatacao(valor, tipo):
    """Aplica formatação baseada no tipo do campo"""
    if valor is None or valor == '':
        return ''
    
    formatadores = {
        'moeda': formatar_moeda,
        'numero': formatar_numero,
        'data': formatar_data,
        'cnpj': formatar_cnpj,
        'cpf': formatar_cpf,
        'cnpj_cpf': formatar_cnpj_cpf,
        'texto': str
    }
    
    formatador = formatadores.get(tipo, str)
    return formatador(valor)

def limpar_chave_nfe(chave):
    """Remove prefixo NFe da chave de acesso"""
    if chave:
        return chave.replace('NFe', '')
    return ''
# xml_extractor.py
"""Módulo para extração de dados de XMLs NF-e"""

import xml.etree.ElementTree as ET
from config import XML_NAMESPACES, CAMPOS_DISPONIVEIS, CAMPOS_PRODUTOS
from utils import aplicar_formatacao, limpar_chave_nfe

class NFeExtractor:
    """Classe para extrair dados de XMLs NF-e"""
    
    def __init__(self, campos_selecionados_notas=None, campos_selecionados_produtos=None, formatar=True):
        self.ns = XML_NAMESPACES
        self.campos_notas = campos_selecionados_notas or []
        self.campos_produtos = campos_selecionados_produtos or []
        self.formatar = formatar
        
        # Cria dicionário unificado de campos
        self.campos_config_notas = {}
        for categoria in CAMPOS_DISPONIVEIS.values():
            self.campos_config_notas.update(categoria)
        
        self.campos_config_produtos = CAMPOS_PRODUTOS
    
    def _extrair_texto(self, element, path):
        """Extrai texto de um elemento XML usando path"""
        if element is None:
            return ''
        
        # Trata casos especiais
        if path.startswith('@'):
            # Atributo
            attr_name = path[1:]
            return element.get(attr_name, '').replace('NFe', '')
        
        # Trata múltiplos caminhos (CNPJ|CPF)
        if '|' in path:
            for p in path.split('|'):
                result = self._extrair_texto(element, p)
                if result:
                    return result
            return ''
        
        # Busca com e sem namespace
        found = element.find(f'.//nfe:{path}', self.ns)
        if found is None:
            found = element.find(f'.//{path}')
        
        return found.text if found is not None else ''
    
    def extrair_dados_nota(self, xml_content, arquivo_nome=''):
        """Extrai dados da nota fiscal"""
        try:
            root = ET.fromstring(xml_content)
            inf_nfe = root.find('.//nfe:infNFe', self.ns) or root.find('.//infNFe')
            
            if inf_nfe is None:
                return None
            
            dados = {'Arquivo': arquivo_nome}
            
            # Extrai campos selecionados
            for campo_id in self.campos_notas:
                if campo_id in self.campos_config_notas:
                    config = self.campos_config_notas[campo_id]
                    label = config['label']
                    path = config['path']
                    tipo = config['tipo']
                    
                    # Tratamento especial para chave
                    if campo_id == 'chave':
                        valor = limpar_chave_nfe(inf_nfe.get('Id', ''))
                    else:
                        valor = self._extrair_texto(inf_nfe, path)
                    
                    # Aplica formatação se habilitado
                    if self.formatar:
                        valor = aplicar_formatacao(valor, tipo)
                    
                    dados[label] = valor
            
            return dados
            
        except Exception as e:
            print(f"Erro ao processar XML: {str(e)}")
            return None
    
    def extrair_produtos(self, xml_content, dados_nota):
        """Extrai produtos da nota fiscal"""
        try:
            root = ET.fromstring(xml_content)
            inf_nfe = root.find('.//nfe:infNFe', self.ns) or root.find('.//infNFe')
            
            if inf_nfe is None:
                return []
            
            produtos = []
            dets = inf_nfe.findall('.//nfe:det', self.ns) or inf_nfe.findall('.//det')
            
            for det in dets:
                produto = {}
                
                # Adiciona referência à nota
                if 'Número NF' in dados_nota:
                    produto['NF Número'] = dados_nota['Número NF']
                if 'Chave de Acesso' in dados_nota:
                    produto['NF Chave'] = dados_nota['Chave de Acesso']
                produto['Arquivo'] = dados_nota.get('Arquivo', '')
                
                # Extrai campos selecionados
                for campo_id in self.campos_produtos:
                    if campo_id in self.campos_config_produtos:
                        config = self.campos_config_produtos[campo_id]
                        label = config['label']
                        path = config['path']
                        tipo = config['tipo']
                        
                        valor = self._extrair_texto(det, path)
                        
                        # Aplica formatação se habilitado
                        if self.formatar:
                            valor = aplicar_formatacao(valor, tipo)
                        
                        produto[label] = valor
                
                produtos.append(produto)
            
            return produtos
            
        except Exception as e:
            print(f"Erro ao processar produtos: {str(e)}")
            return []
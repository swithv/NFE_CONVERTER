# file_processor.py
"""Módulo para processamento de arquivos ZIP e XML"""

import zipfile
import streamlit as st
from xml_extractor import NFeExtractor

class FileProcessor:
    """Classe para processar arquivos XML e ZIP"""
    
    def __init__(self, campos_notas, campos_produtos, formatar=True):
        self.extractor = NFeExtractor(campos_notas, campos_produtos, formatar)
    
    def processar_zip(self, zip_file):
        """Processa arquivos XML dentro de um ZIP"""
        todas_notas = []
        todos_produtos = []
        
        with zipfile.ZipFile(zip_file, 'r') as z:
            xml_files = [f for f in z.namelist() if f.endswith('.xml')]
            
            if not xml_files:
                st.warning("⚠️ Nenhum arquivo XML encontrado no ZIP.")
                return todas_notas, todos_produtos
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, filename in enumerate(xml_files):
                status_text.text(f"🔄 Processando: {filename} ({idx+1}/{len(xml_files)})")
                
                try:
                    with z.open(filename) as xml_file:
                        xml_content = xml_file.read()
                        
                        # Extrai dados da nota
                        dados_nota = self.extractor.extrair_dados_nota(xml_content, filename)
                        
                        if dados_nota:
                            todas_notas.append(dados_nota)
                            
                            # Extrai produtos
                            produtos = self.extractor.extrair_produtos(xml_content, dados_nota)
                            todos_produtos.extend(produtos)
                
                except Exception as e:
                    st.warning(f"⚠️ Erro ao processar {filename}: {str(e)}")
                
                progress_bar.progress((idx + 1) / len(xml_files))
            
            status_text.empty()
            progress_bar.empty()
        
        return todas_notas, todos_produtos
    
    def processar_arquivos_individuais(self, uploaded_files):
        """Processa arquivos XML individuais"""
        todas_notas = []
        todos_produtos = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"🔄 Processando: {uploaded_file.name} ({idx+1}/{len(uploaded_files)})")
            
            try:
                xml_content = uploaded_file.read()
                
                # Extrai dados da nota
                dados_nota = self.extractor.extrair_dados_nota(xml_content, uploaded_file.name)
                
                if dados_nota:
                    todas_notas.append(dados_nota)
                    
                    # Extrai produtos
                    produtos = self.extractor.extrair_produtos(xml_content, dados_nota)
                    todos_produtos.extend(produtos)
            
            except Exception as e:
                st.warning(f"⚠️ Erro ao processar {uploaded_file.name}: {str(e)}")
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        status_text.empty()
        progress_bar.empty()
        
        return todas_notas, todos_produtos
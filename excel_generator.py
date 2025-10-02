# excel_generator.py
"""Módulo para geração de arquivos Excel"""

import pandas as pd
from io import BytesIO
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

class ExcelGenerator:
    """Classe para gerar arquivos Excel formatados"""
    
    def __init__(self):
        self.cor_header = "0000CC"
        self.cor_texto_header = "FFFFFF"
    
    def criar_excel(self, df_notas, df_produtos, incluir_resumo=True):
        """Cria arquivo Excel com múltiplas abas e formatação"""
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Aba de notas fiscais
            if not df_notas.empty:
                df_notas.to_excel(writer, sheet_name='Notas Fiscais', index=False)
                self._formatar_planilha(writer.sheets['Notas Fiscais'])
            
            # Aba de produtos
            if not df_produtos.empty:
                df_produtos.to_excel(writer, sheet_name='Produtos', index=False)
                self._formatar_planilha(writer.sheets['Produtos'])
            
            # Aba de resumo estatístico
            if incluir_resumo and not df_notas.empty:
                df_resumo = self._gerar_resumo(df_notas, df_produtos)
                df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
                self._formatar_planilha(writer.sheets['Resumo'])
        
        output.seek(0)
        return output
    
    def _gerar_resumo(self, df_notas, df_produtos):
        """Gera dados de resumo estatístico"""
        resumo_data = {
            'Métrica': ['Total de Notas', 'Total de Produtos'],
            'Valor': [len(df_notas), len(df_produtos)]
        }
        
        # Identifica colunas de valores (que começam com "R$")
        colunas_valor = []
        for col in df_notas.columns:
            if df_notas[col].dtype == 'object':
                sample = df_notas[col].iloc[0] if len(df_notas) > 0 else ''
                if isinstance(sample, str) and sample.startswith('R$'):
                    colunas_valor.append(col)
        
        # Adiciona totais de valores
        for col in colunas_valor:
            try:
                # Remove formatação para somar
                valores = df_notas[col].str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.')
                total = valores.astype(float).sum()
                resumo_data['Métrica'].append(f'Total {col}')
                resumo_data['Valor'].append(f'R$ {total:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.'))
            except:
                pass
        
        return pd.DataFrame(resumo_data)
    
    def _formatar_planilha(self, worksheet):
        """Aplica formatação à planilha"""
        # Estilo do cabeçalho
        header_fill = PatternFill(start_color=self.cor_header, end_color=self.cor_header, fill_type="solid")
        header_font = Font(bold=True, color=self.cor_texto_header, size=11)
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # Borda
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Formata cabeçalho
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = thin_border
        
        # Ajusta largura das colunas
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # Congela primeira linha
        worksheet.freeze_panes = 'A2'
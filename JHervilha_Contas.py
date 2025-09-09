# ------------------------------------------------------
# JHervilha - Contas
# Autor: Andrews Alves
# Objetivo:
#   - Ler faturas CAIXA e BB em PDF
#   - Extrair Data, Descrição, Valor, Categoria, Subcategoria e Banco
#   - Categorizar automaticamente com base em regex/palavras-chave
#   - Exportar resultados para Excel (Controle Financeiro - JHervilha.xlsx)
#   - Criar backup .txt e logs de execução
#   - Exibir mensagem final com resumo dos registros
# ------------------------------------------------------

import os
import re
import pdfplumber
import pandas as pd
from datetime import datetime
from tkinter import messagebox, Tk

# ================================
# 🔹 Dicionário de categorização
# ================================
CATEGORIAS = {
    r"RESTAURANTE|LANCHONETE|PIZZARIA": ("Alimentação", "Restaurantes"),
    r"MERCADO|SUPERMERCADO|ASSAI|CARREFOUR|EXTRA|PÃO DE AÇÚCAR": ("Alimentação", "Supermercados"),
    r"DROGARIA|DROGASIL|FARMACIA": ("Saúde", "Medicamentos"),
    r"POSTO|GASOLINA|AUTO POSTO": ("Transporte", "Combustível"),
    r"UBER|99|CABIFY": ("Transporte", "Mobilidade"),
    r"RENNE|RIACHUELO|C&A|LOJAS": ("Vestuário", "Roupas"),
}

# ================================
# 🔹 Função categorizadora
# ================================
def categorizar(descricao):
    for padrao, (cat, sub) in CATEGORIAS.items():
        if re.search(padrao, descricao, re.IGNORECASE):
            return cat, sub
    return "Análise Manual", "Verificar"

# ================================
# 🔹 Parser BB
# ================================
def parse_bb(pdf_path):
    registros = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            linhas = page.extract_text().split("\n")
            for linha in linhas:
                # Exemplo esperado: "15/08 Restaurante X 123,45"
                match = re.match(r"(\d{2}/\d{2}) (.+?) (\d+,\d{2})", linha)
                if match:
                    data, desc, valor = match.groups()
                    cat, sub = categorizar(desc)
                    registros.append([data, desc, valor, cat, sub, "BB"])
    return registros

# ================================
# 🔹 Parser CAIXA
# ================================
def parse_caixa(pdf_path):
    registros = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            linhas = page.extract_text().split("\n")
            for linha in linhas:
                # Exemplo esperado: "22/06 MERCADO XYZ 123,45D"
                match = re.match(r"(\d{2}/\d{2}) (.+?) (\d+,\d{2})[DC]?", linha)
                if match:
                    data, desc, valor = match.groups()
                    cat, sub = categorizar(desc)
                    registros.append([data, desc, valor, cat, sub, "CAIXA"])
    return registros

# ================================
# 🔹 Função principal
# ================================
def main():
    # Criar pastas se não existirem
    for pasta in ["FATURAS", "BACKUP", "LOGS"]:
        os.makedirs(pasta, exist_ok=True)

    registros_totais = []
    resumo = []
    log_msgs = []
    data_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for fatura in os.listdir("FATURAS"):
        if fatura.endswith(".pdf"):
            caminho = os.path.join("FATURAS", fatura)
            try:
                if "BB" in fatura.upper():
                    registros = parse_bb(caminho)
                elif "CAIXA" in fatura.upper():
                    registros = parse_caixa(caminho)
                else:
                    continue

                registros_totais.extend(registros)
                resumo.append(f"{fatura}: {len(registros)} registros")
                log_msgs.append(f"[{data_exec}] Processado {fatura} ({len(registros)} registros)")
            except Exception as e:
                log_msgs.append(f"[{data_exec}] Erro em {fatura}: {str(e)}")

    # Salvar Excel
    if registros_totais:
        df = pd.DataFrame(registros_totais, columns=["Data", "Descrição", "Valor", "Categoria", "Subcategoria", "Banco"])
        arquivo_excel = "Controle Financeiro - JHervilha.xlsx"
        with pd.ExcelWriter(arquivo_excel, mode="a", if_sheet_exists="overlay") as writer:
            mes_ano = datetime.now().strftime("%m-%Y")
            df.to_excel(writer, sheet_name=mes_ano, index=False)

        # Backup TXT
        backup_nome = f"BACKUP/{mes_ano}_backup.txt"
        df.to_csv(backup_nome, sep=";", index=False)

    # Log
    with open("LOGS/execucao_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write("\n".join(log_msgs) + "\n")

    # Caixa de mensagem final
    Tk().withdraw()
    if registros_totais:
        messagebox.showinfo("JHervilha - Contas", "✅ Processamento concluído!\n\n" + "\n".join(resumo))
    else:
        messagebox.showerror("JHervilha - Contas", "⚠ Nenhum registro processado.")

if __name__ == "__main__":
    main()

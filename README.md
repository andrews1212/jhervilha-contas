# JHervilha – Contas 💰📊

Automação para extração de faturas **CAIXA** e **BB** (PDF), com:
- **Leitura robusta** por banco (funções `parse_bb()` e `parse_caixa()`).
- **Categorização automática** (regras por palavras-chave).
- **Fallback “Análise Manual / Verificar”** para qualquer linha fora do padrão (nada se perde).
- **Consolidação em Excel** (`Controle Financeiro - JHervilha.xlsx`) criando a aba do mês automaticamente.
- **Backups** por fatura (TXT) com contagem de registros.
- **Logs** detalhados de execução (arquivos `.log` por run).
- **Mensagem final** de sucesso/erro com resumo por fatura.

---

## 📂 Estrutura de Pastas (após a primeira execução)



> **Importante:** As pastas **FATURAS**, **BACKUP**, **LOGS** e **DEBUG** são criadas automaticamente.  
> Se desejar, você pode criá-las antes manualmente; não é obrigatório.

---

## 🚀 Como usar (usuária final)

1. Abra a pasta `dist/`.
2. Dê **dois cliques** em `JHervilha_Contas.exe`.
3. O programa:
   - lê os PDFs em `FATURAS/`,
   - extrai e categoriza os lançamentos,
   - cria/atualiza a aba do mês no Excel `Controle Financeiro - JHervilha.xlsx`,
   - salva backup em `BACKUP/`,
   - registra o log em `LOGS/`,
   - e mostra uma **mensagem final** com o total de linhas por fatura (inclui “Análise Manual”).

---

## 🧠 Regras de categorização

- Regras por **palavras-chave** (ex.: “Uber” → Transporte; “Drogasil” → Saúde; “Assaí” → Supermercado; etc.).
- Tudo que **não** bater com os padrões vai para **“Análise Manual / Verificar”** (garante 100% de cobertura).
- Ajuste ou amplie as regras no dicionário de categorias do script (comentado e organizado).

---

## 🔁 Evitar duplicidade (idempotência)

- O script identifica o **mês/ano** da fatura.  
- Se a aba do mês **já existir**, ele **faz upsert** (não duplica linhas com mesma combinação de chaves) ou cria a aba caso não exista.  
- Logs informam quando houve skip/merge.

---

## 🧪 Onde conferir os resultados

- **Excel:** `Controle Financeiro - JHervilha.xlsx` (aba do mês criada/atualizada).
- **Backup:** `BACKUP\AAAA-MM_<BANCO>_backup_<timestamp>.txt`
- **Log:** `LOGS\run_<timestamp>.log` (contém totais por fatura e erros, se houver).

---

## ⚙️ Geração do .exe (desenvolvedor)

Use o atalho `Recriar_EXE.bat` (duplo clique).  
Ele:
- cria/garante a estrutura de pastas,
- instala/atualiza dependências,
- recria o executável com todos os módulos **embutidos** (ex.: `pdfplumber`, `pillow`, `PyPDF2`, etc.),
- limpa `build/` e `dist/` antigos antes de recriar.

**Executável final:** `dist\JHervilha_Contas.exe`

---

## 🆘 Solução de problemas

- **“No module named pdfplumber” no .exe**  
  Rode o `Recriar_EXE.bat` (ele força `--hidden-import=pdfplumber` e congela dependências).
- **Nenhum dado no Excel**  
  Confira se os PDFs corretos estão em `FATURAS/`. Verifique o arquivo de log em `LOGS\...log` para ver o motivo (ex.: padrão de linha fora do esperado, PDF protegido, etc.).
- **Aba inválida (erro de caractere no título)**  
  O script saneia automaticamente (usa `YYYY-MM`). Evite barras “/” no título.

---

## 🔒 Privacidade

- Os PDFs **não** são enviados a nenhum serviço externo.  
- Backups e logs ficam **apenas** na sua máquina, dentro da pasta do projeto.

---

## 📄 Licença

Projeto privado do usuário. Use somente internamente.

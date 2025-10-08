import pandas as pd
from colorama import Fore, Style, init

# Inicializa o colorama pra deixar bonito no terminal
init(autoreset=True)

print(Fore.CYAN + "🚀 Iniciando integração entre 'Tabelas.xlsx' e 'RegraComissao.xlsx' com base no ID...\n")

# Nomes dos arquivos
arquivo_base = "Tabelas.xlsx"
arquivo_comissao = "RegraComissao.xlsx"
arquivo_saida = "ResultadoFinal.xlsx"

try:
    # Lê as duas planilhas
    tabelas = pd.read_excel(arquivo_base)
    comissao = pd.read_excel(arquivo_comissao)

    print(Fore.GREEN + "✅ Planilhas carregadas com sucesso!")
    print(Fore.YELLOW + f"📘 Colunas detectadas em {arquivo_base}: {list(tabelas.columns)}")
    print(Fore.YELLOW + f"📗 Colunas detectadas em {arquivo_comissao}: {list(comissao.columns)}\n")

    # Verifica se ambas possuem a coluna ID
    if "ID" not in tabelas.columns or "ID" not in comissao.columns:
        raise KeyError("❌ Uma das planilhas não possui a coluna 'ID'. Adicione antes de prosseguir.")

    # Faz o merge (junção)
    resultado = pd.merge(tabelas, comissao, on="ID", how="left", suffixes=('_Tabelas', '_Comissao'))

    # Identifica quais IDs não encontraram correspondência
    ids_sem_match = tabelas[~tabelas["ID"].isin(comissao["ID"])]

    # Cria um resumo bonito
    total_tabelas = len(tabelas)
    total_comissao = len(comissao)
    vinculadas = total_tabelas - len(ids_sem_match)

    print(Fore.CYAN + "📊 RESUMO DA INTEGRAÇÃO:")
    print(Fore.WHITE + f"- Registros em Tabelas: {total_tabelas}")
    print(Fore.WHITE + f"- Registros em RegraComissao: {total_comissao}")
    print(Fore.GREEN + f"- Registros vinculados com sucesso: {vinculadas}")
    print(Fore.YELLOW + f"- Registros sem correspondência: {len(ids_sem_match)}\n")

    # Exporta resultado completo + aba com IDs sem match
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        resultado.to_excel(writer, index=False, sheet_name='Resultado Integrado')
        ids_sem_match.to_excel(writer, index=False, sheet_name='IDs sem correspondência')

    print(Fore.GREEN + f"💾 Arquivo final salvo com sucesso: {arquivo_saida}")
    print(Fore.CYAN + "✨ Duas abas criadas: 'Resultado Integrado' e 'IDs sem correspondência'.")

except FileNotFoundError as e:
    print(Fore.RED + f"❌ Erro: Arquivo não encontrado.\n{e}")

except KeyError as e:
    print(Fore.RED + f"❌ Erro: {e}")

except Exception as e:
    print(Fore.RED + f"⚠️ Erro inesperado: {e}")

print(Style.RESET_ALL)

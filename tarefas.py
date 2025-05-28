import json
import os
from datetime import datetime, timedelta 

CAMINHO_DO_ARQUIVO = "data/tarefa.json"

def adicionar_tarefa(titulo, descricao, data, prioridade):
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump([],f)
    
    with open(CAMINHO_DO_ARQUIVO, "r", encoding="utf-8") as f:
        tarefas = json.load(f)

    nova_tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "data": data,  
        "prioridade": prioridade,
        "status": "pendente"  #status padrão
    }
    tarefas.append(nova_tarefa)

    with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf=8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

    print("✅ Tarefa adicionada com sucesso!") 

def listar_tarefas():
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        print("\n❌ Nenhuma tarefa cadastrada.\n")
        return
    
    with open(CAMINHO_DO_ARQUIVO, "r", encoding="utf-8") as f:
        tarefas = json.load(f)

    if not tarefas:
        print("\n📂 Lista de tarefas vazia.\n")
        return
    
    print("\n~~~~ LISTA DE TAREFAS ~~~~")
    for i, tarefa in enumerate(tarefas):
        print(f"\n[{i}] {tarefa['titulo']} - {tarefa['status'].capitalize()}")
        print(f"Descrição: {tarefa['descricao']}")
        print(f"Data: {tarefa['data']}")
        print(f"Prioridade: {tarefa['prioridade']}")

def concluir_tarefa(indice):
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        print("\n❌ Nenhuma tarefa encontrada.\n")
        return

    with open(CAMINHO_DO_ARQUIVO, "r", encoding="utf-8") as f:
        tarefas = json.load(f)

    if 0 <= indice < len(tarefas):
        tarefas[indice]["status"] = "concluída"
        with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, indent=4, ensure_ascii=False)
        print("\n✅ Tarefa marcada como concluída.\n")
    else:
        print("\n❌ Índice inválido.\n")


def excluir_tarefa(indice):
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        print("\n❌ Nenhuma tarefa para excluir.\n")
        return

    with open(CAMINHO_DO_ARQUIVO, "r", encoding="utf-8") as f:
        tarefas = json.load(f)

    if 0 <= indice < len(tarefas):
        tarefa_removida = tarefas.pop(indice)
        with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(tarefas, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Tarefa '{tarefa_removida['titulo']}' excluída com sucesso.\n")
    else:
        print("\n❌ Índice inválido.\n")

def filtrar_tarefas_por_status(status_desejado):
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        print("\n❌ Nenhuma tarefa cadastrada.")
        return
    
    with open(CAMINHO_DO_ARQUIVO, "r", encoding="utf-8") as f:
        tarefas = json.load(f)

    filtradas = [t for t in tarefas if t["status"].lower() == status_desejado.lower()]

    if not filtradas:
        print(f"\n📂 Nenhuma tarefa com status'{status_desejado}'.\n") 
        return

    print(f"\n~~~~ TAREFAS {status_desejado.upper()}S ~~~~")
    for i, tarefa in enumerate(filtradas):
        print(f"\n[{i}] {tarefa['titulo']} - {tarefa['status'].capitalize()}")
        print(f"Descrição: {tarefa['descricao']}")
        print(f"Data: {tarefa['data']}")
        print(f"Prioridade: {tarefa['prioridade']}")

def verificar_prazos():
    if not os.path.exists(CAMINHO_DO_ARQUIVO):    
        return    

    with open(CAMINHO_DO_ARQUIVO, "r", enconding="utf-8") as f:
        tarefas = json.load(f)

    hoje = datetime.today()

    for tarefa in tarefas:
        try:
            data_tarefa = datetime.strptime(tarefa["data"], "%d/%m/%Y")
            dias_restantes = (data_tarefa - hoje).days

            if tarefa["status"] == "concluída":
                continue

            if dias_restantes < 0:
                print(f"🔴 Tarefa VENCIDA: {tarefa['titulo']} (vencida em {tarefa['data']}).")
            elif dias_restantes <=2:
                print(f"🟡 Tarefa próxima do vencimento: {tarefa['titulo']} (vence em{tarefa['data']}).")

        except ValueError:
            print(f"❌ Data inválida na tarefa: {tarefa['titulo']}.")

def ordenar_tarefas(criterio="data"): # Ordenar tarefas por data ou prioridade
    tarefas = carregar_tarefas()
    if tarefas is None:
        print("\n❌ Nenhuma tarefa cadastrada.\n")
        return

    if criterio == "data":
        try:
            tarefas.sort(key=lambda t: datetime.strptime(t["data"], "%d/%m/%Y"))
        except ValueError:
            print("⚠️ Formato de data inválido em alguma tarefa.")
            return
    elif criterio == "prioridade":
        prioridades = {"alta": 1, "média": 2, "baixa": 3}
        tarefas.sort(key=lambda t: prioridades.get(t["prioridade"].lower(), 4))
    else:
        print("❌ Critério de ordenação inválido. Use 'data' ou 'prioridade'.")
        return

    print(f"\n📋 Tarefas ordenadas por {criterio}:")
    for i, tarefa in enumerate(tarefas):
        print(f"\n[{i}] {tarefa['titulo']} - {tarefa['status'].capitalize()}")
        print(f"Descrição: {tarefa['descricao']}")
        print(f"Data: {tarefa['data']}")
        print(f"Prioridade: {tarefa['prioridade']}")

def carregar_tarefas(): # Funções utilitárias para evitar repetição
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        return None
    with open(CAMINHO_DO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_tarefas(tarefas):
    with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)























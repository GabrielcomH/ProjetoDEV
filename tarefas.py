import json
import os

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
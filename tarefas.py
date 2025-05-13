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

def marcar_como_concluida(indice):
    import json

    CAMINHO_DO_ARQUIVO = "data/tarefa.json"
    
    with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf=8") as f:
        tarefa = json.load(f)

    if 0 <= indice < len(tarefa):
        tarefa[indice]["status"] = "concluída"
        with open(CAMINHO_DO_ARQUIVO, "w", encoding="utf=8") as f:
            json.dump(tarefa, f, indent=4, ensure_ascii=False)
        print("\n✅ Tarefa marcada como concluída.\n")
    else:
        print("\n❌ Índice inválido.\n")
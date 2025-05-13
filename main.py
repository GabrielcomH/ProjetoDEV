from tarefas import adicionar_tarefa

def menu_iniciar():
    print("~~~~ Adicionar Nova Tarefa ~~~~")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    data = input("Data (DD/MM/AAAA): ")
    prioridade = ("Prioridade (Alta, Média ou Baixa): ")

    adicionar_tarefa(titulo, descricao, data, prioridade)   

if __name__ == "__main__":
    menu_iniciar()
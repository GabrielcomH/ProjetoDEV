from tarefas import adicionar_tarefa, listar_tarefas, concluir_tarefa, excluir_tarefa

def menu_iniciar():
    print("~~~~ Adicionar Nova Tarefa ~~~~")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    data = input("Data (DD/MM/AAAA): ")
    prioridade = input("Prioridade (Alta, Média ou Baixa): ")

    adicionar_tarefa(titulo, descricao, data, prioridade)   

while True:
    print("\n~~~~ MENU DE OPÇÕES ~~~~")
    print("1. Listar tarefas")
    print("2. Concluir tarefas")
    print("3. Excluir tarefas")
    print("4. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        listar_tarefas()

    elif opcao == "2":
        try:
            indice = int(input("Digite o número da tarefa que deseja concluir: "))
            concluir_tarefa(indice)
        except ValueError:
            print("Digite um número válido.") 

    elif opcao == "3":
        try:
            indice = int(input("Digite o número da tarefa que deseja excluir: "))
        except ValueError:
            print("Digite um número válido.")

    elif opcao == "4":
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")      

if __name__ == "__main__":
    menu_iniciar()
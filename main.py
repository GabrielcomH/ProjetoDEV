from tarefas import (    
    adicionar_tarefa, 
    listar_tarefas, 
    concluir_tarefa, 
    excluir_tarefa, 
    filtrar_tarefas_por_status, 
    verificar_prazos

)

def menu_adicionar_tarefa():
    print("~~~~ Adicionar Nova Tarefa ~~~~")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    data = input("Data (DD/MM/AAAA): ")
    prioridade = input("Prioridade (Alta, Média ou Baixa): ")

    adicionar_tarefa(titulo, descricao, data, prioridade)   

def menu():
    while True:
        print("\n~~~~ MENU DE OPÇÕES ~~~~")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Concluir tarefas")
        print("4. Excluir tarefas")
        print("5. Filtrar tarefas") 
        print("6. Verificar prazos")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_adicionar_tarefa()

        elif opcao == "2":
            listar_tarefas()

        elif opcao == "3":
            try:
                indice = int(input("Digite o número da tarefa que deseja concluir: "))
                concluir_tarefa(indice)
            except ValueError:
                print("Digite um número válido.") 
        elif opcao == "4":
            try:
                indice = int(input("Digite o número da tarefa que deseja excluir: "))
                excluir_tarefa(indice)
            except ValueError:
                print("Digite um número válido.")
        
        elif opcao == "5":
            status = input("Filtrar por qual status (pendente ou concluída)?").lower()
            filtrar_tarefas_por_status(status)

        elif opcao == "6":
            verificar_prazos()

        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")      

if __name__ == "__main__":
    menu()

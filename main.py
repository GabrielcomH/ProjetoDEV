from tarefas import (    
    adicionar_tarefa, 
    listar_tarefas, 
    concluir_tarefa, 
    excluir_tarefa, 
    filtrar_tarefas_por_status, 
    verificar_prazos,
    ordenar_tarefas,
    reabrir_tarefa,
    salvar_tarefas,
    carregar_tarefas
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
        print("5. Filtrar tarefas por status") 
        print("6. Verificar prazos")
        print("7. Ordenar tarefas")
        print("8. Reabrir tarefa")
        print("9. Salvar tarefas")
        print("10. Carregar tarefas")
        print("0. Sair")

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
            print("\nOrdenar tarefas por:")
            print("1. Data")
            print("2. Prioridade")
            escolha_ordenacao = input("Escolha uma opção (1 ou 2): ")

            if escolha_ordenacao == "1":
                ordenar_tarefas(criterio="data")
                listar_tarefas()

            elif escolha_ordenacao == "2":
                ordenar_tarefas(criterio="prioridade")
                listar_tarefas()

            else:
                print("Digite um número válido.")

        elif opcao == "8":
            try:
                indice = int(input("Digite o índice da tarefa que deseja reabrir: "))
                reabrir_tarefa(indice)
            except ValueError:
                print("Digite um número válido.")

        elif opcao == "9":
            tarefas = carregar_tarefas()
            if tarefas is not None:
                salvar_tarefas()
                print("\nTarefas salvas com sucesso!")
            else:
                print("\nNenhuma tarefa para salvar.")

        elif opcao == "10":
            tarefas = carregar_tarefas()
            if tarefas is not None:
                print("\nTarefas carregadas com sucesso!\n")
                listar_tarefas()
            else:
                print("\nNenhuma tarefa encontrada no arquivo.")

        elif opcao == "0":
            print("\nSaindo...\n")
            break

        else:
            print("Opção inválida. Tente novamente.")      

if __name__ == "__main__":
    menu()

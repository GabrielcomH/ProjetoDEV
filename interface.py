import tkinter as tk
from tkinter import messagebox, ttk
import time
from tarefas import (
    adicionar_tarefa,
    listar_tarefas,
    concluir_tarefa,
    excluir_tarefa,
    filtrar_tarefas_por_status,
    verificar_prazos,
    ordenar_tarefas,
    reabrir_tarefa,
    carregar_tarefas,
    salvar_tarefas
)

def splash_screen():
    splash = tk.Tk()
    splash.title("Carregando...")
    splash.geometry("300x150")
    tk.Label(splash, text="Gerenciador de Tarefas", font=("Arial", 18)).pack(expand=True)
    splash.after(2000, splash.destroy)
    splash.mainloop()

def abrir_janela_adicionar():
    janela = tk.Toplevel()
    janela.title("Adicionar Tarefa")
    janela.geometry("300x300")

    tk.Label(janela, text="Título:").pack()
    entrada_titulo = tk.Entry(janela)
    entrada_titulo.pack()

    tk.Label(janela, text="Descrição:").pack()
    entrada_descricao = tk.Entry(janela)
    entrada_descricao.pack()

    tk.Label(janela, text="Data (DD/MM/AAAA):").pack()
    entrada_data = tk.Entry(janela)
    entrada_data.pack()

    tk.Label(janela, text="Prioridade:").pack()
    combo = ttk.Combobox(janela, values=["alta", "média", "baixa"])
    combo.set("média")
    combo.pack()

    def salvar():
        titulo = entrada_titulo.get()
        descricao = entrada_descricao.get()
        data = entrada_data.get()
        prioridade = combo.get()
        if titulo and data and prioridade:
            adicionar_tarefa(titulo, descricao, data, prioridade)
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso.")
            janela.destroy()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos obrigatórios.")

    tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

def executar_funcao_com_indice(funcao, mensagem):
    tarefas = carregar_tarefas()
    if not tarefas:
        messagebox.showinfo("Vazio", "Nenhuma tarefa cadastrada.")
        return

    janela = tk.Toplevel()
    janela.title(mensagem)
    janela.geometry("400x300")

    tk.Label(janela, text="Selecione o índice da tarefa:").pack()
    for i, t in enumerate(tarefas):
        tk.Label(janela, text=f"[{i}] {t['titulo']} - {t['status']}").pack(anchor="w")

    entrada = tk.Entry(janela)
    entrada.pack(pady=10)

    def executar():
        try:
            indice = int(entrada.get())
            funcao(indice)
            janela.destroy()
        except:
            messagebox.showerror("Erro", "Índice inválido.")

    tk.Button(janela, text="Executar", command=executar).pack()

def filtrar_status():
    janela = tk.Toplevel()
    janela.title("Filtrar por Status")
    janela.geometry("250x150")

    tk.Label(janela, text="Status (pendente/concluída):").pack()
    entrada = tk.Entry(janela)
    entrada.pack()

    def filtrar():
        status = entrada.get().strip().lower()
        filtrar_tarefas_por_status(status)

    tk.Button(janela, text="Filtrar", command=filtrar).pack(pady=10)

def ordenar_opcao():
    janela = tk.Toplevel()
    janela.title("Ordenar Tarefas")
    janela.geometry("250x150")

    tk.Label(janela, text="Escolha o critério:").pack()
    combo = ttk.Combobox(janela, values=["data", "prioridade"])
    combo.set("data")
    combo.pack()

    def ordenar():
        criterio = combo.get()
        ordenar_tarefas(criterio)

    tk.Button(janela, text="Ordenar", command=ordenar).pack(pady=10)

def salvar_tarefas_menu():
    tarefas = carregar_tarefas()
    if tarefas:
        salvar_tarefas(tarefas)
        messagebox.showinfo("Salvo", "Tarefas salvas com sucesso.")
    else:
        messagebox.showinfo("Vazio", "Nenhuma tarefa para salvar.")

def carregar_tarefas_menu():
    tarefas = carregar_tarefas()
    if tarefas:
        messagebox.showinfo("Sucesso", "Tarefas carregadas.")
        listar_tarefas()
    else:
        messagebox.showinfo("Vazio", "Nenhuma tarefa encontrada.")

def iniciar_menu():
    root = tk.Tk()
    root.title("Menu Principal")
    root.geometry("400x600")

    botoes = [
        ("➕ Adicionar Tarefa", abrir_janela_adicionar),
        ("📄 Listar Tarefas", listar_tarefas),
        ("✅ Concluir Tarefa", lambda: executar_funcao_com_indice(concluir_tarefa, "Concluir")),
        ("🗑 Excluir Tarefa", lambda: executar_funcao_com_indice(excluir_tarefa, "Excluir")),
        ("🔍 Filtrar por Status", filtrar_status),
        ("📆 Verificar Prazos", verificar_prazos),
        ("↕ Ordenar Tarefas", ordenar_opcao),
        ("🔁 Reabrir Tarefa", lambda: executar_funcao_com_indice(reabrir_tarefa, "Reabrir")),
        ("💾 Salvar Tarefas", salvar_tarefas_menu),
        ("📂 Carregar Tarefas", carregar_tarefas_menu),
        ("🚪 Sair", root.destroy)
    ]

    for texto, comando in botoes:
        tk.Button(root, text=texto, width=35, height=2, command=comando).pack(pady=5)

    root.mainloop()

if __name__ == "_main_":
    splash_screen()
    iniciar_menu()
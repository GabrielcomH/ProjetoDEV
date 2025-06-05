import tkinter as tk
from tkinter import messagebox, ttk
import time
from datetime import datetime, date
from tarefas import (adicionar_tarefa, listar_tarefas, concluir_tarefa, excluir_tarefa, filtrar_tarefas_por_status,
    verificar_prazos, ordenar_tarefas, reabrir_tarefa, carregar_tarefas, salvar_tarefas)

def splash_screen():
    splash = tk.Tk()
    splash.title("Carregando...")
    splash.overrideredirect(True)
    largura, altura = 400, 200
    splash.geometry(f"{largura}x{altura}+{(splash.winfo_screenwidth()-largura)//2}+{(splash.winfo_screenheight()-altura)//2}")
    canvas = tk.Canvas(splash, width=largura, height=altura, bg="#2b5876", highlightthickness=0)
    canvas.pack()
    canvas.create_text(largura//2, altura//3, text="Gerenciador de Tarefas", fill="white", font=("Arial", 20, "bold"))
    ttk.Progressbar(splash, orient="horizontal", length=300, mode="determinate").place(relx=0.5, rely=0.8, anchor="center")
    def animar():
        for i in range(101):
            splash.children['!progressbar']['value'] = i
            splash.update()
            time.sleep(0.03)
        splash.destroy()
    splash.after(100, animar)
    splash.mainloop()

def abrir_janela_adicionar():
    janela = tk.Toplevel()
    janela.title("Adicionar Tarefa")
    janela.geometry("400x500")
    janela.resizable(False, False)
    janela.configure(bg="#f5f5f5")

    main_frame = tk.Frame(janela, bg="#f5f5f5", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text="➕ Nova Tarefa", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 20))
    
    form_frame = tk.Frame(main_frame, bg="#f5f5f5")
    form_frame.pack(fill="x")

    def criar_campo(container, label_text):
        frame = tk.Frame(container, bg="#f5f5f5", pady=8)
        frame.pack(fill="x")
        tk.Label(frame, text=label_text, font=("Arial", 10), bg="#f5f5f5", fg="#34495e").pack(anchor="w")
        if label_text == "Prioridade:":
            combo = ttk.Combobox(frame, values=["Alta", "Média", "Baixa"], font=("Arial", 10), state="readonly")
            combo.set("Média"); combo.pack(fill="x", ipadx=4); return combo
        else:
            entry = tk.Entry(frame, font=("Arial", 10), relief="solid", borderwidth=1)
            entry.pack(fill="x", ipady=4); return entry
        
    entrada_titulo = criar_campo(form_frame, "Título*:")
    entrada_descricao = criar_campo(form_frame, "Descrição:")
    entrada_data = criar_campo(form_frame, "Data (DD/MM/AAAA)*:")

    dica_frame = tk.Frame(form_frame, bg="#f5f5f5")
    dica_frame.pack(fill="x", pady=(0, 10))
    tk.Label(dica_frame, text="Exemplo: 15/06/2024", font=("Arial", 8), bg="#f5f5f5", fg="#7f8c8d").pack(anchor="w")

    entrada_prioridade = criar_campo(form_frame, "Prioridade:")

    btn_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=20)
    btn_frame.pack(fill="x")

    def salvar_tarefa():
        titulo = entrada_titulo.get().strip()
        descricao = entrada_descricao.get().strip()
        data = entrada_data.get().strip()
        prioridade = entrada_prioridade.get().lower()
        if not titulo or not data:
            return messagebox.showwarning("Atenção", "Os campos marcados com * são obrigatórios!")
            
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            return messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA.")
        adicionar_tarefa(titulo, descricao, data, prioridade)
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
        janela.destroy()

    btn_salvar = tk.Button(btn_frame, text="SALVAR TAREFA", command=salvar_tarefa, bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                          relief="flat", padx=20, pady=8, bd=0)
    btn_salvar.pack(side="right", ipadx=10)
    
    btn_cancelar = tk.Button(btn_frame, text="CANCELAR", command=janela.destroy, bg="#e74c3c", fg="white", font=("Arial", 10),
                            relief="flat", padx=20, pady=8, bd=0)
    btn_cancelar.pack(side="left", ipadx=10)

    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (janela.winfo_screenwidth // 2)
    y = (janela.winfo_screenheight() // 2) - (janela.winfo_screenheight // 2)
    janela.geometry(f"+{x}+{y}")
    entrada_titulo.focus_set()

def executar_funcao_com_indice(funcao, mensagem):
    tarefas = carregar_tarefas()
    if not tarefas:
        return messagebox.showinfo("Vazio", "Nenhuma tarefa cadastrada.")

    janela = tk.Toplevel()
    janela.title(f"Ação: {mensagem}")
    janela.geometry("500x450")
    janela.configure(bg="#f0f2f5")
    janela.resizable(False, False)

    main_frame = tk.Frame(janela, bg="#f0f2f5", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text=f"Selecione a tarefa para {mensagem.lower()}:", font=("Arial", 10, "bold"), bg="#f0f2f5", fg="#2c3e50").pack(pady=(0, 15))
    
    lista_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
    lista_frame.pack(fill="both", expand=True, pady=(0, 15))

    scrollbar = tk.Scrollbar(lista_frame)
    scrollbar.pack(side="right", fill="y")

    lista_tarefas = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set,  font=("Arial", 10), selectbackground="#3498db", 
                               selectforeground="white", bg="#ffffff", bd=0, highlightthickness=0)
    lista_tarefas.pack(fill="both", expand=True)
    scrollbar.config(command=lista_tarefas.yview)

    indices_mapeados = []
    for i, tarefa in enumerate(tarefas):
        status = "✓" if tarefa["status"] == "concluída" else "✗"
        cor = "#2ecc71" if tarefa["status"] == "concluída" else "#e74c3c"
        texto = f"[{i}] {tarefa['titulo']} ({tarefa['data']}) - {status}"
        lista_tarefas.insert("end", texto)
        lista_tarefas.itemconfig("end", fg=cor)
        indices_mapeados.append(i)

    input_frame = tk.Frame(main_frame, bg="#f0f2f5")
    input_frame.pack(fill="x", pady=(0, 15))

    tk.Label(input_frame, text="Selecione a tarefa na lista ou digite o índice:", font=("Arial", 10), 
             bg="#f0f2f5").pack(anchor="w")
    entrada = tk.Entry(input_frame, font=("Arial", 10), bd=1, relief="solid", width=10)
    entrada.pack(anchor="w")

    lista_tarefas.bind("<<ListboxSelect>>", lambda e: (entrada.delete(0, tk.END), entrada.insert(0, indices_mapeados[lista_tarefas.curselection()[0]])) if lista_tarefas.curselection() else None)

    def executar():
            try:
                indice = indices_mapeados[lista_tarefas.curselection()[0]] if lista_tarefas.curselection() else int(entrada.get())
                if indice not in indices_mapeados: raise ValueError
                funcao(indice)
                messagebox.showinfo("Sucesso", f"Tarefa {mensagem.lower()} com sucesso!")
                janela.destroy()
                if mensagem == "Excluir": listar_tarefas
            except:
                messagebox.showerror("Erro", "Índice inválido ou tarefa não está na lista!")

    btn_frame = tk.Frame(janela, bg="#f0f2f5")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text=mensagem, command=executar, bg="#3498db", fg="white", font=("Arial", 10), padx=20,
              pady=5, relief="flat").pack(side="right")
    tk.Button(btn_frame, text="Cancelar", command=janela.destroy, bg="#95a5a6", fg="white", font=("Arial", 10), padx=20,
              pady=5, relief="flat").pack(side="right", padx=10)
    
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (janela.winfo_screenwidth() // 2)
    y = (janela.winfo_screenheight() // 2) - (janela.winfo_screenheight() // 2)
    janela.geometry(f"+{x}+{y}")
    entrada.focus_set()

def ordenar_opcao():
    try:
        tarefas = carregar_tarefas()
        if not tarefas:
            return messagebox.showinfo("Info", "Nenhuma tarefa cadastrada.")
        
        janela = tk.Toplevel()
        janela.title("Ordenar Tarefas")
        janela.geometry("400x250")
        janela.resizable(False, False)
        janela.configure(bg="#f5f5f5")

        main_frame = tk.Frame(janela, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="Ordenar Tarefas por Prazo", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 20))

        ordenar_por = tk.StringVar(value="prioridade")

        opcoes_frame = tk.Frame(main_frame, bg="#f5f5f5")
        opcoes_frame.pack(fill="x", pady=10)

        tk.Radiobutton(opcoes_frame, text="Ordenar por Prioridade (Alta > Média > Baixa)", variable=ordenar_por,
                      value="prioridade", bg="#f5f5f5").pack(anchor="w", pady=5)

        tk.Radiobutton(opcoes_frame, text="Ordenar por Data (Mais próxima primeiro)", variable=ordenar_por,
                      value="data", bg="#f5f5f5").pack(anchor="w", pady=5)

        btn_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=20)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="ORDENAR", command=lambda: mostrar_resultados(ordenar_por.get(), janela), bg="#3498db",
                 fg="white", font=("Arial", 10, "bold"), relief="flat", padx=20, pady=8).pack(side="left", padx=5, ipadx=10)

        tk.Button(btn_frame, text="SAIR", command=janela.destroy, bg="#95a5a6", fg="white", font=("Arial", 10),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5, ipadx=10)

        janela.update_idletasks()
        x = (janela.winfo_screenwidth() // 2) - (janela.winfo_screenwidth()// 2)
        y = (janela.winfo_screenheight() // 2) - (janela.winfo_screenheight() // 2)
        janela.geometry(f"+{x}+{y}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ordenar tarefas: {str(e)}")

def mostrar_resultados(ordenar_por, janela_anterior):
    try:
        tarefas = carregar_tarefas()
        hoje = datetime.today()
        
        tarefas = [t for t in tarefas if t["status"] != "concluída"]

        tarefas_com_dias = []
        for t in tarefas:
            try:
                data_tarefa = datetime.strptime(t["data"], "%d/%m/%Y")
                dias = (data_tarefa - hoje).days
                tarefas_com_dias.append((t, dias))
            except ValueError:
                print(f"Data inválida: {t['titulo']}")
        
        if ordenar_por == "prioridade":
            prioridades = {"alta": 1, "média": 2, "baixa": 3}
            tarefas_ordenadas = sorted(tarefas_com_dias, key=lambda x: prioridades.get(x[0]["prioridade"].lower(), 4))
            titulo = "Tarefas Ordenadas por Prioridade"
        else:
            tarefas_ordenadas = sorted(tarefas_com_dias, key=lambda x: datetime.strptime(x[0]["data"], "%d/%m/%Y"))
            titulo = "Tarefas Ordenadas por Data"
        
        janela = tk.Toplevel()
        janela.title(titulo)
        janela.geometry("800x600")
        janela.configure(bg="#f5f5f5")

        main_frame = tk.Frame(janela, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text=titulo, font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 15))

        text_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        text_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Consolas", 10), padx=10,
                            pady=10, bg="#ffffff", bd=0)
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        cores = {
            "vencidas": ("#e74c3c", "Vencidas"), "proximas": ("#f39c12", "Próximas do vencimento"),
            "normais": ("#2ecc71", "Prazos normais")}
        
        for cat, (cor, texto) in cores.items():
            text_widget.tag_config(cat, foreground=cor)
            text_widget.tag_config(f"{cat}_header", foreground=cor, font=("Consolas", 10, "bold"))

        categorias = {
            "vencidas": [t for t in tarefas_ordenadas if t[1] < 0], "proximas": [t for t in tarefas_ordenadas if 0 <= t[1] <= 2],
            "normais": [t for t in tarefas_ordenadas if t[1] > 2]}

        for cat, (cor, texto) in cores.items():
            if categorias[cat]:
                text_widget.insert("end", f"{texto}:\n", f"{cat}_header")
                for tarefa, dias in categorias[cat]:
                    status = f"(Venceu há {-dias} dias)" if dias < 0 else f"(Vence em {dias} dias)"
                    text_widget.insert("end", f"  • {tarefa['titulo']} {status}\n", cat)
                    text_widget.insert("end", f"    Data: {tarefa['data']}\n", cat)
                    text_widget.insert("end", f"    Prioridade: {tarefa['prioridade'].capitalize()}\n\n", cat)
                text_widget.insert("end", "\n")

        text_widget.configure(state="disabled")

        tk.Button(main_frame, text="SAIR", command=janela.destroy, bg="#95a5a6", fg="white", font=("Arial", 10),
                 relief="flat", padx=20, pady=8).pack(pady=(15, 0))

        janela.update_idletasks()
        x = (janela.winfo_screenwidth() // 2) - (janela.winfo_screenwidth() // 2)
        y = (janela.winfo_screenheight() // 2) - (janela.winfo_screenheight() // 2)
        janela.geometry(f"+{x}+{y}")
        janela_anterior.destroy()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao mostrar resultados: {str(e)}")

def filtrar_status():
    def mostrar_tarefas_filtradas(status_selecionado):
        tarefas = carregar_tarefas()
        tarefas_filtradas = [t for t in tarefas if t["status"] == status_selecionado]
        
        janela_resultado = tk.Toplevel()
        janela_resultado.title(f"Tarefas {status_selecionado.capitalize()}s")
        janela_resultado.geometry("600x500")
        janela_resultado.configure(bg="#f5f5f5")
        janela_resultado.resizable(False, False)

        main_frame = tk.Frame(janela_resultado, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text=f"📋 Tarefas {status_selecionado.capitalize()}s", font=("Arial", 14, "bold"), bg="#f5f5f5",
                fg="#2c3e50").pack(pady=(0, 15))

        if not tarefas_filtradas:
            tk.Label(main_frame, text=f"Nenhuma tarefa {status_selecionado} encontrada.", font=("Arial", 10), bg="#f5f5f5").pack()
            return

        list_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        texto = tk.Text(list_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 10), padx=10, pady=10, bg="#ffffff", bd=0)
        texto.pack(fill="both", expand=True)
        scrollbar.config(command=texto.yview)

        for i, tarefa in enumerate(tarefas_filtradas, 1):
            texto.insert("end", f"Tarefa {i}:\n", "bold")
            texto.insert("end", f"• Título: {tarefa['titulo']}\n")
            texto.insert("end", f"• Descrição: {tarefa['descricao']}\n")
            texto.insert("end", f"• Data: {tarefa['data']}\n")
            texto.insert("end", f"• Prioridade: {tarefa['prioridade']}\n")
            texto.insert("end", f"• Status: {tarefa['status']}\n", "status")
            texto.insert("end", "-"*50 + "\n\n")

        texto.tag_config("bold", font=("Arial", 10, "bold"))
        texto.tag_config("status", font=("Arial", 10, "bold"))
        texto.configure(state="disabled")

        janela_resultado.update_idletasks()
        x = (janela_resultado.winfo_screenwidth() // 2) - (janela_resultado.winfo_screenwidth() // 2)
        y = (janela_resultado.winfo_screenheight() // 2) - (janela_resultado.winfo_screenheight() // 2)
        janela_resultado.geometry(f"+{x}+{y}")

    janela = tk.Toplevel()
    janela.title("Filtrar Tarefas por Status")
    janela.geometry("350x250")
    janela.resizable(False, False)
    janela.configure(bg="#f5f5f5")

    main_frame = tk.Frame(janela, bg="#f5f5f5", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text="🔍 Filtrar Tarefas por Status", font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 20))

    form_frame = tk.Frame(main_frame, bg="#f5f5f5")
    form_frame.pack(fill="x")

    tk.Label(form_frame, text="Selecione o status:", font=("Arial", 10), bg="#f5f5f5").pack(anchor="w", pady=(0, 5))

    combo_status = ttk.Combobox(form_frame, values=["pendente", "concluída"], font=("Arial", 10), state="readonly")
    combo_status.set("pendente")
    combo_status.pack(fill="x", pady=(0, 20))

    btn_frame = tk.Frame(main_frame, bg="#f5f5f5", pady=10)
    btn_frame.pack(fill="x")

    def aplicar_filtro():
        status_selecionado = combo_status.get().strip()
        if status_selecionado in ["pendente", "concluída"]:
            janela.destroy()
            mostrar_tarefas_filtradas(status_selecionado)
        else:
            messagebox.showwarning("Aviso", "Selecione um status válido!")

    tk.Button(btn_frame, text="APLICAR FILTRO", command=aplicar_filtro, bg="#3498db", fg="white", font=("Arial", 10, "bold"),
             relief="flat", padx=20, pady=5).pack(side="right", ipadx=10)

    tk.Button(btn_frame, text="CANCELAR", command=janela.destroy, bg="#95a5a6", fg="white", font=("Arial", 10),
             relief="flat", padx=20, pady=5).pack(side="right", padx=10)

    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (janela.winfo_screenwidth() // 2)
    y = (janela.winfo_screenheight() // 2) - (janela.winfo_screenheight() // 2)
    janela.geometry(f"+{x}+{y}")
    combo_status.focus_set()
    
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
        
def verificar_prazos():
    try:
        tarefas = carregar_tarefas()
        if not tarefas:
            messagebox.showinfo("Info", "Nenhuma tarefa cadastrada.")
            return
        
        hoje = datetime.today()
        categorias = {"Vencidas": {"cor": "#e74c3c", "dias": lambda d: d < 0, "itens": []}, "Próximas do Vencimento": {"cor": "#f39c12", "dias": lambda d: 0 <= d <= 2, "itens": []},
            "Normais": {"cor": "#2ecc71", "dias": lambda d: d > 2, "itens": []}}
        
        for tarefa in tarefas:
            if tarefa["status"] == "concluída":
                continue
            try:
                data_tarefa = datetime.strptime(tarefa["data"], "%d/%m/%Y")
                dias = (data_tarefa - hoje).days
                for cat, config in categorias.items():
                    if config["dias"](dias):
                        config["itens"].append((tarefa, dias))
                        break
            except ValueError:
                print(f"Data inválida: {tarefa['titulo']}")
        
        janela_resultado = tk.Toplevel()
        janela_resultado.title("Status de Prazos das Tarefas")
        janela_resultado.geometry("700x500")
        janela_resultado.configure(bg="#f5f5f5")
        
        main_frame = tk.Frame(janela_resultado, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        tk.Label(main_frame, text="Status de Prazos das Tarefas", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 15))
        
        text_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Consolas", 10),
                            padx=10, pady=10, bg="#ffffff", bd=0)
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        for cat, config in categorias.items():
            text_widget.tag_config(cat, foreground=config["cor"])
        
        for cat, config in categorias.items():
            if config["itens"]:
                text_widget.insert("end", f"{cat}:\n", (cat, "bold"))
                for tarefa, dias in config["itens"]:
                    status = f"(Venceu há {-dias} dias)" if dias < 0 else f"(Vence em {dias} dias)"
                    text_widget.insert("end", f"  • {tarefa['titulo']} {status}\n", cat)
                    text_widget.insert("end", f"    Data: {tarefa['data']}\n", cat)
                    text_widget.insert("end", f"    Prioridade: {tarefa['prioridade']}\n\n", cat)
                text_widget.insert("end", "\n")
        
        text_widget.tag_config("bold", font=("Consolas", 10, "bold"))
        text_widget.configure(state="disabled")
        
        janela_resultado.update_idletasks()
        x = (janela_resultado.winfo_screenwidth() // 2) - (janela_resultado.winfo_screenwidth() // 2)
        y = (janela_resultado.winfo_screenheight() // 2) - (janela_resultado.winfo_screenheight() // 2)
        janela_resultado.geometry(f"+{x}+{y}")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar prazos: {str(e)}")

def concluir_tarefa_interface():

    tarefas = carregar_tarefas()
    if not tarefas:
        return messagebox.showinfo("Info", "Não há tarefas cadastradas")
    
    janela = tk.Toplevel()
    janela.title("Concluir Tarefa")
    janela.geometry("600x500")
    janela.resizable(False, False)

    main_frame = tk.Frame(janela, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text="Selecione a tarefa para concluir:", font=("Arial", 12)).pack(pady=10)

    lista_frame = tk.Frame(main_frame)
    lista_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(lista_frame)
    scrollbar.pack(side="right", fill="y")

    lista = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set, font=("Arial", 10), selectbackground="#3498db", selectforeground="white")
    
    tarefas_pendentes = []
    for i, tarefa in enumerate(tarefas):
        if tarefa["status"] == "pendente":
            lista.insert("end", f"{i}: {tarefa['titulo']} (Prazo: {tarefa['data']})")
            tarefas_pendentes.append(i)

    lista.pack(fill="both", expand=True)
    scrollbar.config(command=lista.yview)

    def confirmar():
        selecao = lista.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
            return
            
        indice_real = tarefas_pendentes[selecao[0]]
        sucesso, mensagem = concluir_tarefa(indice_real)
        
        if sucesso:
            titulo_tarefa = tarefas[indice_real]['titulo']
            messagebox.showinfo("Tarefa Concluída", 
                              f"A tarefa '{titulo_tarefa}' foi concluída com sucesso!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", mensagem)

    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(pady=20, fill="x")

    btn_concluir = tk.Button(btn_frame, text="CONCLUIR TAREFA", command=confirmar, bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                             relief="flat",padx=20,pady=8,bd=0)
    btn_concluir.pack(side="right", ipadx=10)

    btn_cancelar = tk.Button(btn_frame, text="CANCELAR", command=janela.destroy, bg="#e74c3c", fg="white", font=("Arial", 10),
        relief="flat", padx=20, pady=8, bd=0)
    btn_cancelar.pack(side="left", ipadx=10)

def listar_tarefas():
    tarefas = carregar_tarefas()
    
    janela = tk.Toplevel()
    janela.title("Lista de Tarefas")
    janela.geometry("700x600")
    janela.configure(bg="#f5f5f5")
    janela.resizable(False, False)

    main_frame = tk.Frame(janela, bg="#f5f5f5", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    tk.Label(main_frame, text="📋 Lista Completa de Tarefas", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#2c3e50").pack(pady=(0, 15))

    if not tarefas:
        tk.Label(main_frame,
                text="Nenhuma tarefa cadastrada.",
                font=("Arial", 10),
                bg="#f5f5f5").pack()
        return

    list_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
    list_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    texto = tk.Text(list_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 10), padx=10, pady=10, bg="#ffffff", bd=0)
    texto.pack(fill="both", expand=True)
    scrollbar.config(command=texto.yview)

    for i, tarefa in enumerate(tarefas):
        status_color = "#e74c3c" if tarefa["status"] == "pendente" else "#2ecc71"
        
        texto.insert("end", f"Tarefa {i}:\n", "bold")
        texto.insert("end", f"• Título: {tarefa['titulo']}\n")
        texto.insert("end", f"• Descrição: {tarefa['descricao']}\n")
        texto.insert("end", f"• Data: {tarefa['data']}\n")
        texto.insert("end", f"• Prioridade: {tarefa['prioridade']}\n")
        texto.insert("end", "• Status: ")
        texto.insert("end", f"{tarefa['status']}\n", ("status", status_color))
        texto.insert("end", "-"*50 + "\n\n")

    texto.tag_config("bold", font=("Arial", 10, "bold"))
    texto.tag_config("status", font=("Arial", 10, "bold"))
    texto.tag_config("#e74c3c", foreground="#e74c3c")
    texto.tag_config("#2ecc71", foreground="#2ecc71")
    texto.configure(state="disabled")

    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (janela.winfo_screenwidth() // 2)
    y = (janela.winfo_screenheight() // 2) - (janela.winfo_screenheight() // 2)
    janela.geometry(f"+{x}+{y}")

def reabrir_tarefa_interface():
    janela = tk.Toplevel()
    janela.title("Reabrir Tarefa")
    janela.geometry("500x300")
    janela.configure(bg="#ffffff")

    frame = tk.Frame(janela, bg="#ffffff")
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    lista = tk.Listbox(frame, yscrollcommand=scrollbar.set, bg="#ffffff", font=("Arial", 10))
    scrollbar.pack(side="right", fill="y")
    lista.pack(fill="both", expand=True)
    scrollbar.config(command=lista.yview)

    try:
        tarefas = carregar_tarefas() or []
        indices = [i for i, t in enumerate(tarefas) 
                 if isinstance(t, dict) and t.get("status") == "concluída"]
        
        if not indices:
            messagebox.showinfo("Info", "Nenhuma tarefa concluída disponível.")
            janela.destroy()
            return
            
        for i in indices:
            t = tarefas[i]
            lista.insert("end", f"{t.get('titulo', 'Sem título')} (concluída em: {t.get('data_conclusao', 'data desconhecida')})")

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar tarefas: {str(e)}")
        janela.destroy()
        return

    def confirmar():
        if not (sel := lista.curselection()):
            messagebox.showwarning("Aviso", "Selecione uma tarefa!")
            return
            
        idx = indices[sel[0]]
        try:
            if tarefas[idx]["status"] != "concluída":
                messagebox.showerror("Erro", "Tarefa já está aberta!")
                return
                
            tarefas[idx]["status"] = "pendente"
            salvar_tarefas(tarefas)
            messagebox.showinfo("Sucesso", "Tarefa reaberta com sucesso!")
            janela.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na reabertura: {str(e)}")

    tk.Button(janela, text="Reabrir Tarefa", command=confirmar,
             bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
             relief="flat", padx=10, pady=5).pack(pady=10)

def iniciar_menu():

    root = tk.Tk()
    root.title("Menu Principal - Gerenciador de Tarefas")
    root.geometry("500x650")
    root.configure(bg="#f0f2f5")
    
    main_frame = tk.Frame(root, bg="#f0f2f5")
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    title_frame = tk.Frame(main_frame, bg="#2b5876")
    title_frame.pack(fill="x", pady=(0, 20))
    
    tk.Label(title_frame, text="Gerenciador de Tarefas", font=("Arial", 18, "bold"), fg="white", bg="#2b5876").pack(pady=10)
    
    def criar_botao(frame, texto, comando, cor):
        btn = tk.Button(frame, text=texto, command=comando, width=25, height=2, font=("Arial", 10), bg=cor, fg="white",
                       activebackground=cor, activeforeground="white", relief="flat", borderwidth=0, highlightthickness=0)
        btn.pack(pady=5, padx=10)
        return btn
    
    cores = {
        "adicionar": "#27ae60", "listar": "#2980b9", "concluir": "#f39c12", "excluir": "#e74c3c", "filtrar": "#9b59b6",
        "prazos": "#1abc9c", "ordenar": "#34495e", "reabrir": "#e67e22", "salvar": "#16a085", "carregar": "#7f8c8d", "sair": "#95a5a6"}
    
    botoes_operacoes = [
        ("➕ Adicionar Tarefa", abrir_janela_adicionar, cores["adicionar"]),
        ("📄 Listar Tarefas", listar_tarefas, cores["listar"]),
        ("✅ Concluir Tarefa", lambda: concluir_tarefa_interface(), cores["concluir"]),
        ("🗑 Excluir Tarefa", lambda: executar_funcao_com_indice(excluir_tarefa, "Excluir"), cores["excluir"])]
    
    botoes_organizacao = [
        ("🔍 Filtrar por Status", filtrar_status, cores["filtrar"]),
        ("📆 Verificar Prazos", verificar_prazos, cores["prazos"]),
        ("↕ Ordenar Tarefas", ordenar_opcao, cores["ordenar"]),
        ("🔁 Reabrir Tarefa", reabrir_tarefa_interface, cores["reabrir"])]
    
    botoes_arquivo = [
        ("💾 Salvar Tarefas", salvar_tarefas_menu, cores["salvar"]),
        ("📂 Carregar Tarefas", carregar_tarefas_menu, cores["carregar"]),
        ("🚪 Sair", root.destroy, cores["sair"])]
    
    frame_operacoes = tk.LabelFrame(main_frame, text=" Operações ", font=("Arial", 10), bg="#f0f2f5", fg="#2c3e50")
    frame_operacoes.pack(fill="x", pady=5)
    
    frame_organizacao = tk.LabelFrame(main_frame, text=" Organização ", font=("Arial", 10), bg="#f0f2f5", fg="#2c3e50")
    frame_organizacao.pack(fill="x", pady=5)
    
    frame_arquivo = tk.LabelFrame(main_frame, text=" Arquivo ", font=("Arial", 10), bg="#f0f2f5", fg="#2c3e50")
    frame_arquivo.pack(fill="x", pady=5)
    
    for texto, comando, cor in botoes_operacoes:
        criar_botao(frame_operacoes, texto, comando, cor)
    
    for texto, comando, cor in botoes_organizacao:
        criar_botao(frame_organizacao, texto, comando, cor)
    
    for texto, comando, cor in botoes_arquivo:
        criar_botao(frame_arquivo, texto, comando, cor)
    
    tk.Label(main_frame, text="© 2024 Gerenciador de Tarefas v2.0", font=("Arial", 8), fg="#7f8c8d", bg="#f0f2f5").pack(side="bottom", pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    splash_screen()
    iniciar_menu()
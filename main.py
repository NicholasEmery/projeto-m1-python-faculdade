import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from pymongo import MongoClient

class SistemaOcorrencias:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['ouvidoria']
        self.collection = self.db['ocorrencias']

    def exibir_ocorrencias(self):
        ocorrencias = self.collection.find()
        return [{"cpf": o["cpf"], "tipo": o["tipo"], "descricao": o["descricao"]} for o in ocorrencias]

    def adicionar_ocorrencia(self, cpf, tipo, descricao):
        if len(cpf) != 11:
            raise ValueError("CPF Invalido!")
        elif not cpf.isdigit():
            raise ValueError("O CPF deve conter apenas números!")
        
        ocorrencia = {"cpf": int(cpf), "tipo": tipo, "descricao": descricao}
        self.collection.insert_one(ocorrencia)

    def exibir_ocorrencias_por_cpf(self, cpf):
        ocorrencias = self.collection.find({"cpf": int(cpf)})
        return [{"cpf": o["cpf"], "tipo": o["tipo"], "descricao": o["descricao"]} for o in ocorrencias]

    def exibir_ocorrencias_por_tipo(self, tipo):
        ocorrencias = self.collection.find({"tipo": (tipo)})
        return [{"cpf": o["cpf"], "tipo": o["tipo"], "descricao": o["descricao"]} for o in ocorrencias]

    def excluir_todas_ocorrencias(self):
        self.collection.delete_many({})

    def excluir_ocorrencia_por_cpf(self, cpf):
        self.collection.delete_one({"cpf": int(cpf)})

    def atualizar_ocorrencia(self, cpf, tipo, descricao):
        self.collection.update_one({"cpf": int(cpf)}, {"$set": {"tipo": tipo, "descricao": descricao}})


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.cpf = None
        self.descricao = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Digite seu CPF (11 dígitos):").grid(row=0, column=0, padx=5, pady=5)
        self.cpf_entry = ttk.Entry(master)
        self.cpf_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
        self.descricao_entry = ttk.Entry(master)
        self.descricao_entry.grid(row=1, column=1, padx=5, pady=5)
        return self.cpf_entry  # initial focus

    def apply(self):
        self.cpf = self.cpf_entry.get()
        self.descricao = self.descricao_entry.get()

    def get_values(self):
        return self.cpf, self.descricao


class SelectOcorrenciaDialog(simpledialog.Dialog):
    def __init__(self, parent, ocorrencias, title=None):
        self.ocorrencias = ocorrencias
        self.selected_ocorrencia = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="Selecione a ocorrência para atualizar:").pack(padx=10, pady=10)

        self.ocorrencia_listbox = tk.Listbox(master)
        for idx, ocorrencia in enumerate(self.ocorrencias):
            self.ocorrencia_listbox.insert(tk.END, f"{idx+1}. Tipo: {ocorrencia['tipo']}, Descrição: {ocorrencia['descricao']}")
        self.ocorrencia_listbox.pack(padx=10, pady=10)

    def apply(self):
        selected_index = self.ocorrencia_listbox.curselection()
        if selected_index:
            self.selected_ocorrencia = self.ocorrencias[selected_index[0]]

    def get_selected_ocorrencia(self):
        return self.selected_ocorrencia


class UpdateDialog(simpledialog.Dialog):
    def __init__(self, parent, ocorrencia, title=None):
        self.ocorrencia = ocorrencia
        self.tipo = None
        self.descricao = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text=f"CPF: {self.ocorrencia['cpf']}").grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(master, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_entry = ttk.Entry(master)
        self.tipo_entry.insert(0, self.ocorrencia["tipo"])
        self.tipo_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Descrição:").grid(row=2, column=0, padx=5, pady=5)
        self.descricao_entry = ttk.Entry(master)
        self.descricao_entry.insert(0, self.ocorrencia["descricao"])
        self.descricao_entry.grid(row=2, column=1, padx=5, pady=5)

    def apply(self):
        self.tipo = self.tipo_entry.get()
        self.descricao = self.descricao_entry.get()

    def get_values(self):
        return self.tipo, self.descricao


class OuvidoriaApp:
    def __init__(self, root):
        self.sistema = SistemaOcorrencias()
        self.root = root
        self.root.title("UNIFACISA")

        # Definindo o ícone da aplicação na barra de tarefas
        self.root.iconbitmap('images/facisaicon.ico')

        # Configurar fundo sólido azul escuro
        self.root.configure(bg='dark blue')

        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = ttk.Frame(self.root, style="Header.TFrame")
        self.header_frame.pack(pady=10)

        # Logotipo da FACISA
        self.logo_img = Image.open("images/Facisa.png")
        self.logo_img = self.logo_img.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = ttk.Label(self.header_frame, image=self.logo_photo, style="Header.TLabel")
        self.logo_label.pack()

        self.university_frame = ttk.Frame(self.header_frame, style="Header.TFrame")
        self.university_frame.pack()

        self.uni_label = ttk.Label(self.university_frame, text="UNIFACISA", font=("Helvetica", 16), foreground="white", style="Header.TLabel")
        self.uni_label.pack(side="left")

        self.title_label = ttk.Label(self.header_frame, text="SISTEMA DE OUVIDORIA", font=("Helvetica", 14), foreground="white", style="Header.TLabel")
        self.title_label.pack()

        # Botões do MENU - configuração
        self.button_frame = ttk.Frame(self.root, style="Menu.TFrame")
        self.button_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton",
                        font=("Helvetica", 12),
                        padding=10)
        
        style.configure("Header.TFrame", background="dark blue")
        style.configure("Header.TLabel", background="dark blue", foreground="white")
        style.configure("Menu.TFrame", background="dark blue")
        
        style.map("TButton",
                  background=[('active', '#0052cc'), ('!active', 'white')],
                  foreground=[('active', 'white'), ('!active', 'black')])

        self.elogio_img = Image.open("images/elogio.png").resize((50, 50), Image.LANCZOS)
        self.elogio_photo = ImageTk.PhotoImage(self.elogio_img)
        self.critica_img = Image.open("images/critica.png").resize((50, 50), Image.LANCZOS)
        self.critica_photo = ImageTk.PhotoImage(self.critica_img)
        self.sugestao_img = Image.open("images/sugestao.png").resize((50, 50), Image.LANCZOS)
        self.sugestao_photo = ImageTk.PhotoImage(self.sugestao_img)

        self.elogio_btn = ttk.Button(self.button_frame, text="ELOGIO", image=self.elogio_photo, compound="top", command=lambda: self.adicionar_ocorrencia("ELOGIO"), style="TButton")
        self.elogio_btn.grid(row=0, column=0, padx=10, pady=10)

        self.critica_btn = ttk.Button(self.button_frame, text="CRÍTICA", image=self.critica_photo, compound="top", command=lambda: self.adicionar_ocorrencia("CRÍTICA"), style="TButton")
        self.critica_btn.grid(row=0, column=1, padx=10, pady=10)

        self.sugestao_btn = ttk.Button(self.button_frame, text="SUGESTÃO", image=self.sugestao_photo, compound="top", command=lambda: self.adicionar_ocorrencia("SUGESTÃO"), style="TButton")
        self.sugestao_btn.grid(row=0, column=2, padx=10, pady=10)

        self.listar_btn = ttk.Button(self.button_frame, text="Listar todas as ocorrências", command=self.listar_ocorrencias, style="TButton")
        self.listar_btn.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.exibir_usuario_btn = ttk.Button(self.button_frame, text="Exibir ocorrências por CPF", command=self.exibir_por_cpf, style="TButton")
        self.exibir_usuario_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.excluir_todas_btn = ttk.Button(self.button_frame, text="Excluir todas as ocorrências", command=self.excluir_todas, style="TButton")
        self.excluir_todas_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.excluir_por_cpf_btn = ttk.Button(self.button_frame, text="Excluir ocorrência por CPF", command=self.excluir_por_cpf, style="TButton")
        self.excluir_por_cpf_btn.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.atualizar_btn = ttk.Button(self.button_frame, text="Atualizar ocorrência por CPF", command=self.atualizar_ocorrencia, style="TButton")
        self.atualizar_btn.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Frame para o botão de sair no canto inferior direito
        self.exit_frame = ttk.Frame(self.root, style="Menu.TFrame")
        self.exit_frame.pack(side="bottom", anchor="e", padx=10, pady=10)

        self.sair_btn = ttk.Button(self.exit_frame, text="Sair", command=self.root.quit, style="TButton")
        self.sair_btn.pack()

        # Adicionar eventos de mudança de cor nos botões
        for btn in self.button_frame.winfo_children():
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        e.widget.config(background='#0052cc', foreground='white')

    def on_leave(self, e):
        e.widget.config(background='white', foreground='black')

    def listar_ocorrencias(self):
        ocorrencias = self.sistema.exibir_ocorrencias()
        self.mostrar_ocorrencias(ocorrencias)

    def adicionar_ocorrencia(self, tipo):
        dialog = CustomDialog(self.root, f"Adicionar {tipo}")
        cpf, descricao = dialog.get_values()

        if cpf and descricao:
            try:
                self.sistema.adicionar_ocorrencia(cpf, tipo, descricao)
                messagebox.showinfo("Sucesso", f"{tipo} adicionada com sucesso.")
            except ValueError as e:
                messagebox.showerror("Erro", str(e))

    def exibir_por_cpf(self):
        cpf = self.input_dialog("Exibir Ocorrências por CPF", "Digite um CPF:")
        if cpf:
            ocorrencias = self.sistema.exibir_ocorrencias_por_cpf(cpf)
            self.mostrar_ocorrencias(ocorrencias)

    def excluir_todas(self):
        self.sistema.excluir_todas_ocorrencias()
        messagebox.showinfo("Sucesso", "Todas as ocorrências foram excluídas.")

    def excluir_por_cpf(self):
        cpf = self.input_dialog("Excluir Ocorrência", "Digite o CPF da ocorrência a ser excluída:")
        if cpf:
            self.sistema.excluir_ocorrencia_por_cpf(cpf)
            messagebox.showinfo("Sucesso", f"Ocorrência '{cpf}' foi excluída.")

    def atualizar_ocorrencia(self):
        cpf = self.input_dialog("Atualizar Ocorrência", "Digite o CPF da ocorrência a ser atualizada:")
        if cpf:
            ocorrencias = self.sistema.exibir_ocorrencias_por_cpf(cpf)
            if ocorrencias:
                select_dialog = SelectOcorrenciaDialog(self.root, ocorrencias, "Selecione Ocorrência")
                ocorrencia = select_dialog.get_selected_ocorrencia()
                if ocorrencia:
                    update_dialog = UpdateDialog(self.root, ocorrencia, "Atualizar Ocorrência")
                    tipo, descricao = update_dialog.get_values()
                    if tipo and descricao:
                        self.sistema.atualizar_ocorrencia(cpf, tipo, descricao)
                        messagebox.showinfo("Sucesso", f"Ocorrência atualizada com sucesso.")
            else:
                messagebox.showinfo("Erro", "Nenhuma ocorrência encontrada para o CPF fornecido.")

    def input_dialog(self, title, prompt):
        input_value = simpledialog.askstring(title, prompt)
        return input_value

    def mostrar_ocorrencias(self, ocorrencias):
        if ocorrencias:
            ocorrencias_text = "\n\n".join([f"CPF: {o['cpf']}, Tipo: {o['tipo']}, Descrição: {o['descricao']}" for o in ocorrencias])
        else:
            ocorrencias_text = "Nenhuma ocorrência encontrada."
        messagebox.showinfo("Ocorrências", ocorrencias_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = OuvidoriaApp(root)
    root.mainloop()

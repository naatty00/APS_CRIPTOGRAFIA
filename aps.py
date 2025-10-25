import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter.ttk import Checkbutton

import string
import random
import json
import os

def gerar_chave():
    letras = list(string.ascii_uppercase)
    embaralhadas = letras.copy()
    random.shuffle(embaralhadas)
    chave = dict(zip(letras, embaralhadas))
    return chave

def salvar_chave(chave, nome_arquivo="chave.json"):
    diretorio = os.path.dirname(nome_arquivo)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)
    with open(nome_arquivo, "w") as f:
        json.dump(chave, f)

def carregar_chave(nome_arquivo="chave.json"):
    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                else:
                    print(f"Warning: Conteúdo de {nome_arquivo} não é um dicionário.")
                    return None
        except json.JSONDecodeError as e:
             print(f"Erro ao decodificar JSON em {nome_arquivo}: {e}")
             raise
        except Exception as e:
            print(f"Erro inesperado ao ler chave de {nome_arquivo}: {e}")
            raise
    else:
        return None

def criptografar(texto, chave):
    resultado = ''
    if not isinstance(chave, dict):
        messagebox.showerror("Erro de Chave", "Nenhuma chave válida carregada para criptografar.")
        return texto

    for char in texto.upper():
        if char in chave:
            resultado += chave[char]
        else:
            resultado += char
    return resultado

def inverter_chave(chave):
    if isinstance(chave, dict):
        return {v: k for k, v in chave.items()}
    return {}

def descriptografar(texto_cifrado, chave):
    chave_inversa = inverter_chave(chave)
    resultado = ''
    if not isinstance(chave, dict) or not chave_inversa :
        messagebox.showerror("Erro de Chave", "Nenhuma chave válida carregada para descriptografar.")
        return texto_cifrado

    for char in texto_cifrado.upper():
        if char in chave_inversa:
            resultado += chave_inversa[char]
        else:
            resultado += char
    return resultado

class CryptoApp:
    def __init__(self, root):

        self.MAIN_BG = "#000000"
        self.TEXT_BOX_BG = "#1C1C1C"
        self.NEON_TEXT = "#00FFFF"
        self.BUTTON_BLUE = "#70DFFF"
        self.LABEL_TEXT = "#D0D0D0"

        self.root = root

        self.root.title("SISTEMA CRIPTOGRÁFICO")
        self.root.geometry("600x550")

        try:
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            self.script_dir = os.getcwd()

        self.nome_arquivo_chave = "chave.json"
        self.caminho_completo_chave = os.path.join(self.script_dir, self.nome_arquivo_chave)

        try:
            icon_path = os.path.join(self.script_dir, "icone.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"--- ERRO AO CARREGAR 'icone.ico' ---")
            print(f"Erro: {e}")
            print(f"Verifique se o arquivo 'icone.ico' está em: {self.script_dir}")

        self.root.configure(bg=self.MAIN_BG)
        self.chave = None
        self.limit_warning_shown = False

        style = tb.Style.get_instance()

        default_font = ('Arial', 10)
        self.root.option_add('*TFont', default_font)

        style.configure('TFrame', background=self.MAIN_BG)
        style.configure('secondary.TFrame', background=self.MAIN_BG)
        style.configure('TLabel', font=default_font, foreground=self.LABEL_TEXT, background=self.MAIN_BG)
        style.configure('info.TLabel', font=('Arial', 10, 'bold'), foreground=self.NEON_TEXT, background=self.MAIN_BG)
        style.configure('danger.TLabel', font=('Arial', 10, 'bold'), background=self.MAIN_BG)
        style.configure('TEntry',
                        fieldbackground=self.TEXT_BOX_BG,
                        foreground=self.NEON_TEXT,
                        insertcolor=self.NEON_TEXT,
                        font=('Arial', 10))
        style.configure('custom.Outline.TButton',
                        font=('Arial', 11, 'bold'),
                        foreground=self.BUTTON_BLUE,
                        background=self.MAIN_BG,
                        borderwidth=2)
        style.map('custom.Outline.TButton',
                  background=[('active', self.BUTTON_BLUE), ('hover', self.BUTTON_BLUE)],
                  foreground=[('active', self.MAIN_BG), ('hover', self.MAIN_BG)])
        style.configure('small.custom.Outline.TButton',
                        font=('Arial', 9, 'bold'),
                        foreground=self.BUTTON_BLUE,
                        background=self.MAIN_BG,
                        borderwidth=2)
        style.map('small.custom.Outline.TButton',
                  background=[('active', self.BUTTON_BLUE), ('hover', self.BUTTON_BLUE)],
                  foreground=[('active', self.MAIN_BG), ('hover', self.MAIN_BG)])
        style.configure('custom.TCheckbutton',
                        font=('Arial', 10),
                        foreground=self.BUTTON_BLUE,
                        background=self.MAIN_BG)
        style.map('custom.TCheckbutton',
                  foreground=[('active', self.NEON_TEXT), ('hover', self.NEON_TEXT)],
                  background=[('active', self.MAIN_BG), ('hover', self.MAIN_BG)])

        scroll_container = ScrolledFrame(root, autohide=True, padding=(10, 15))
        scroll_container.pack(fill='both', expand=True)

        input_frame = tb.Frame(scroll_container, padding=(10, 0))
        input_frame.pack(fill='x', expand=False, pady=(0, 5))

        input_header_frame = tb.Frame(input_frame)
        input_header_frame.pack(fill='x', expand=True, pady=(0, 5))

        tb.Label(input_header_frame, text="Entrada de Dados (Máx. 128 caracteres):").pack(side='left', anchor='w')

        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=5,
                                                     bg=self.TEXT_BOX_BG, fg=self.NEON_TEXT,
                                                     insertbackground=self.NEON_TEXT,
                                                     font=('Arial', 11),
                                                     bd=1, relief='solid')
        self.input_text.pack(fill='x', expand=True)

        self.input_text.bind("<KeyRelease>", self.check_input_limit)
        self.input_text.bind("<<Paste>>", self.check_input_limit)

        action_frame = tb.Frame(scroll_container, padding=(10, 10))
        action_frame.pack(fill='x', expand=False, pady=(5, 5))
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.encrypt_button = tb.Button(action_frame, text="Criptografar",
                                        command=self.encrypt_action,
                                        style='custom.Outline.TButton')
        self.encrypt_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        self.decrypt_button = tb.Button(action_frame, text="Descriptografar",
                                        command=self.decrypt_action,
                                        style='custom.Outline.TButton')
        self.decrypt_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))

        output_frame = tb.Frame(scroll_container, padding=(10, 0))
        output_frame.pack(fill='x', expand=False, pady=(5, 5))

        output_header_frame = tb.Frame(output_frame)
        output_header_frame.pack(fill='x', expand=True, pady=(0, 5))
        tb.Label(output_header_frame, text="Resultado:").pack(side='left', anchor='w')

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=5,
                                                      bg=self.TEXT_BOX_BG, fg=self.NEON_TEXT,
                                                      insertbackground=self.NEON_TEXT,
                                                      font=('Arial', 11),
                                                      bd=1, relief='solid',
                                                      state='disabled')
        self.output_text.pack(fill='x', expand=True)

        self.move_to_input_button = tb.Button(output_frame,
                                              text="\u21C5 Mover",
                                              command=self.move_output_to_input,
                                              style='small.custom.Outline.TButton')
        self.move_to_input_button.pack(side='right', anchor='se', pady=(5, 0), padx=5)

        self.show_adv_var = tk.BooleanVar(value=False)
        self.adv_checkbutton = tb.Checkbutton(scroll_container,
                                              text="Mostrar Opções Avançadas",
                                              variable=self.show_adv_var,
                                              command=self.toggle_advanced_options,
                                              style='custom.TCheckbutton')
        self.adv_checkbutton.pack(anchor='w', pady=(10, 0), padx=10)

        self.key_frame = tb.Frame(scroll_container, padding=(10, 5))

        tb.Label(self.key_frame, text="Arquivo da Chave:").pack(anchor='w', pady=(0, 5))
        key_inner_frame = tb.Frame(self.key_frame)
        key_inner_frame.pack(fill='x')
        self.key_file_var = tk.StringVar(value=self.nome_arquivo_chave)
        self.key_entry = tb.Entry(key_inner_frame, textvariable=self.key_file_var,
                                  font=('Arial', 10), state='readonly')
        self.key_entry.pack(side='left', fill='x', expand=True, ipady=4, padx=(0, 10))
        self.load_key_button = tb.Button(key_inner_frame, text="Carregar Chave",
                                         command=self.load_key_from_file_dialog,
                                         style='custom.Outline.TButton')
        self.load_key_button.pack(side='left', padx=5)
        self.gen_key_button = tb.Button(key_inner_frame, text="Gerar Nova",
                                        command=self.gen_key_action,
                                        style='custom.Outline.TButton')
        self.gen_key_button.pack(side='left', padx=(5, 0))

        self.status_label = tb.Label(scroll_container, text="Carregue ou gere uma chave para começar.",
                                     style='danger.TLabel', padding=(10, 10))
        self.status_label.pack(fill='x', expand=False, pady=(10, 0))

        self.load_default_key_on_start()

    def toggle_advanced_options(self):
        if self.show_adv_var.get():
            self.key_frame.pack(fill='x', expand=False, pady=(0, 5), padx=10, before=self.status_label)
        else:
            self.key_frame.pack_forget()

    def move_output_to_input(self):
        output_text = self.output_text.get("1.0", tk.END).strip()
        if not output_text:
            messagebox.showwarning("Resultado Vazio", "Não há nada no campo de resultado para mover.")
            return
        try:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", output_text)
            self.check_input_limit()
        except Exception as e:
            messagebox.showerror("Erro ao Mover", f"Não foi possível mover o texto: {e}")

    def check_input_limit(self, event=None):
        try:
            text = self.input_text.get("1.0", "end-1c")
            length = len(text)
            if length > 128:
                cursor_pos = self.input_text.index(tk.INSERT)
                text = text[:128]
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", text)
                if self.input_text.compare(cursor_pos, ">", "1.128"):
                    self.input_text.mark_set(tk.INSERT, "1.128")
                else:
                    self.input_text.mark_set(tk.INSERT, cursor_pos)
                if not self.limit_warning_shown:
                    messagebox.showwarning("Limite Atingido",
                                         "A entrada de dados está limitada a 128 caracteres.")
                    self.limit_warning_shown = True
                self.update_status("ERRO: Limite de 128 caracteres atingido.", "danger")
            else:
                self.limit_warning_shown = False
                if "Limite" in self.status_label.cget("text"):
                    self.update_key_status()
        except Exception as e:
            print(f"Erro no check_input_limit: {e}")

    def update_key_status(self):
        if not self.limit_warning_shown:
            if self.chave:
                file_display_name = os.path.basename(self.caminho_completo_chave)
                self.update_status(f"✅ Chave '{file_display_name}' carregada com sucesso.", "info")
            else:
                self.update_status(f"⚠️ Nenhuma chave '{self.nome_arquivo_chave}' encontrada ou selecionada. Gere uma nova.", "danger")

    def gen_key_action(self):
        try:
            self.caminho_completo_chave = os.path.join(self.script_dir, "chave.json")
            self.nome_arquivo_chave = "chave.json"
            self.key_file_var.set(self.nome_arquivo_chave)

            self.chave = gerar_chave()
            salvar_chave(self.chave, self.caminho_completo_chave)
            self.update_key_status()
            messagebox.showinfo("Sucesso", f"Nova chave gerada e salva com sucesso em:\n{self.caminho_completo_chave}")
        except Exception as e:
            messagebox.showerror("Erro ao Gerar Chave", f"Não foi possível gerar ou salvar a chave:\n{e}")

    def _load_key_logic(self, file_path):
        chave_carregada_com_sucesso = False
        try:
            chave_data = carregar_chave(file_path)
            if chave_data is not None:
                 self.chave = chave_data
                 self.caminho_completo_chave = file_path
                 self.nome_arquivo_chave = os.path.basename(file_path)
                 self.key_file_var.set(self.nome_arquivo_chave)
                 chave_carregada_com_sucesso = True
            else:
                 self.chave = None
                 if os.path.exists(file_path):
                     messagebox.showerror("Erro de Formato", f"O arquivo '{os.path.basename(file_path)}' não contém um dicionário de chave válido.")

            self.update_key_status()

            if chave_carregada_com_sucesso:
                 messagebox.showinfo("Sucesso", f"Chave carregada com sucesso de:\n{file_path}")

        except json.JSONDecodeError as e:
             messagebox.showerror("Erro ao Carregar Chave", f"Erro ao decodificar o arquivo '{os.path.basename(file_path)}'.\nNão parece ser um JSON válido.\nDetalhe: {e}")
             self.chave = None
             self.caminho_completo_chave = os.path.join(self.script_dir, "chave.json")
             self.nome_arquivo_chave = "chave.json"
             self.key_file_var.set(self.nome_arquivo_chave)
             self.update_key_status()
        except Exception as e:
            messagebox.showerror("Erro ao Carregar Chave", f"Não foi possível ler o arquivo da chave:\n{e}")
            self.chave = None
            self.caminho_completo_chave = os.path.join(self.script_dir, "chave.json")
            self.nome_arquivo_chave = "chave.json"
            self.key_file_var.set(self.nome_arquivo_chave)
            self.update_key_status()

    def load_key_from_file_dialog(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Arquivo da Chave",
            initialdir=self.script_dir,
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")]
        )
        if file_path:
            self._load_key_logic(file_path)
        else:
             print("Seleção de arquivo cancelada.")

    def load_default_key_on_start(self):
         default_path = os.path.join(self.script_dir, "chave.json")
         if os.path.exists(default_path):
             try:
                 chave_data = carregar_chave(default_path)
                 if chave_data is not None:
                      self.chave = chave_data
                      self.caminho_completo_chave = default_path
                      self.nome_arquivo_chave = "chave.json"
                      self.key_file_var.set(self.nome_arquivo_chave)
                      print(f"Chave padrão '{self.nome_arquivo_chave}' carregada ao iniciar.")
                 else:
                     self.chave = None
             except Exception as e:
                 print(f"Erro ao carregar chave padrão no início: {e}")
                 self.chave = None
         else:
             self.chave = None
         self.update_key_status()

    def encrypt_action(self):
        if not self.chave:
            messagebox.showwarning("Chave não Encontrada", "Por favor, carregue ou gere uma chave primeiro.")
            return
        plain_text = self.input_text.get("1.0", tk.END).strip()
        if not plain_text:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para criptografar.")
            return
        try:
            cipher_text = criptografar(plain_text, self.chave)
            self.display_output(cipher_text)
        except Exception as e:
            messagebox.showerror("Erro de Criptografia", f"Ocorreu um erro: {e}")

    def decrypt_action(self):
        if not self.chave:
            messagebox.showwarning("Chave não Encontrada", "Por favor, carregue ou gere uma chave primeiro.")
            return
        cipher_text = self.input_text.get("1.0", tk.END).strip()
        if not cipher_text:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para descriptografar.")
            return
        try:
            plain_text = descriptografar(cipher_text, self.chave)
            if plain_text != cipher_text or self.chave :
                self.display_output(plain_text)
        except Exception as e:
            messagebox.showerror("Erro de Descriptografia", f"Ocorreu um erro: {e}")

    def display_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", text)
        self.output_text.config(state='disabled')

    def update_status(self, message, style_color):
        self.status_label.config(text=message, bootstyle=style_color)

if __name__ == "__main__":
    app = tb.Window(themename="superhero")
    CryptoApp(app)
    app.mainloop()

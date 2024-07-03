import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import threading
import json
import os

class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Talisman Online Auto Login")
        self.root.geometry("300x500") 
        
        self.jogo_executavel = ""
        self.pasta_jogo = ""
        self.quantidade_contas = 1
        self.contas = []

        self.frame_botoes = tk.Frame(root)
        self.frame_botoes.pack(expand=True, pady=50) 

        self.iniciar_btn = tk.Button(self.frame_botoes, text="Iniciar", command=self.iniciar_bot, width=20)
        self.iniciar_btn.pack(pady=10)  
        
        self.configuracoes_btn = tk.Button(self.frame_botoes, text="Configurações", command=self.abrir_configuracoes, width=20)
        self.configuracoes_btn.pack(pady=10)  
        
        self.sair_btn = tk.Button(self.frame_botoes, text="Sair", command=root.quit, width=20)
        self.sair_btn.pack(pady=10) 

        self.carregar_configuracoes()

    def carregar_configuracoes(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.jogo_executavel = config.get('jogo_executavel', "")
                self.pasta_jogo = config.get('pasta_jogo', "")
                self.quantidade_contas = config.get('quantidade_contas', 1)
                self.contas = config.get('contas', [])
        except FileNotFoundError:
            pass

    def abrir_configuracoes(self):
        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("Configurações")
        self.config_window.geometry("400x400") 
        
        config_frame = tk.Frame(self.config_window)
        config_frame.pack(expand=True)

        tk.Label(config_frame, text="Pasta do Jogo:").pack(pady=5)
        self.pasta_jogo_entry = tk.Entry(config_frame, width=50)
        self.pasta_jogo_entry.insert(0, self.pasta_jogo)
        self.pasta_jogo_entry.pack(pady=5)
        tk.Button(config_frame, text="Selecionar Pasta", command=self.selecionar_pasta_jogo).pack(pady=5)
        
        tk.Label(config_frame, text="Executável do Jogo:").pack(pady=5)
        self.jogo_executavel_entry = tk.Entry(config_frame, width=50)
        self.jogo_executavel_entry.insert(0, self.jogo_executavel)
        self.jogo_executavel_entry.pack(pady=5)
        tk.Button(config_frame, text="Selecionar Executável", command=self.selecionar_executavel).pack(pady=5)
        
        tk.Label(config_frame, text="Quantidade de Contas:").pack(pady=5)
        self.quantidade_contas_entry = tk.Entry(config_frame, width=5)
        self.quantidade_contas_entry.insert(0, str(self.quantidade_contas))
        self.quantidade_contas_entry.pack(pady=5)
        tk.Button(config_frame, text="Contas", command=self.abrir_janela_contas).pack(pady=5)
        
        tk.Button(config_frame, text="Salvar", command=self.salvar_configuracoes).pack(pady=10)

    def selecionar_pasta_jogo(self):
        pasta_jogo = filedialog.askdirectory()
        if pasta_jogo:
            self.pasta_jogo_entry.delete(0, tk.END)
            self.pasta_jogo_entry.insert(0, pasta_jogo)

    def selecionar_executavel(self):
        executavel = filedialog.askopenfilename(filetypes=[("Executáveis", "*.exe")])
        if executavel:
            self.jogo_executavel_entry.delete(0, tk.END)
            self.jogo_executavel_entry.insert(0, executavel)

    def abrir_janela_contas(self):
        self.contas_window = tk.Toplevel(self.root)
        self.contas_window.title("Contas")
        self.contas_window.geometry("400x400")  

        contas_frame = tk.Frame(self.contas_window)
        contas_frame.pack(expand=True)

        self.contas_entries = []
        for i in range(self.quantidade_contas):
            conta_info = {}
            tk.Label(contas_frame, text=f"Conta {i+1} Usuário:").pack(pady=5)
            conta_info['usuario'] = tk.Entry(contas_frame, width=20)
            conta_info['usuario'].pack(pady=5)
            
            tk.Label(contas_frame, text=f"Conta {i+1} Senha:").pack(pady=5)
            conta_info['senha'] = tk.Entry(contas_frame, width=20, show="*")
            conta_info['senha'].pack(pady=5)
            
            if i < len(self.contas):
                conta_info['usuario'].insert(0, self.contas[i]['usuario'])
                conta_info['senha'].insert(0, self.contas[i]['senha'])
            
            self.contas_entries.append(conta_info)
        
        tk.Button(contas_frame, text="Salvar", command=self.salvar_contas).pack(pady=10)

    def salvar_contas(self):
        self.contas = [
            {
                'usuario': conta['usuario'].get(),
                'senha': conta['senha'].get()
            }
            for conta in self.contas_entries
        ]
        self.contas_window.destroy()
        messagebox.showinfo("Contas", "Contas salvas com sucesso!")
        
    def salvar_configuracoes(self):
        self.pasta_jogo = self.pasta_jogo_entry.get()
        self.jogo_executavel = self.jogo_executavel_entry.get()
        try:
            self.quantidade_contas = int(self.quantidade_contas_entry.get())
        except ValueError:
            self.quantidade_contas = 1

        config = {
            'pasta_jogo': self.pasta_jogo,
            'jogo_executavel': self.jogo_executavel,
            'quantidade_contas': self.quantidade_contas,
            'contas': self.contas
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f)
        
        messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")

    def iniciar_bot(self):
        if not self.jogo_executavel or not os.path.isfile(self.jogo_executavel):
            messagebox.showerror("Erro", "O executável do jogo não foi selecionado ou não existe.")
            return
        
        if not self.pasta_jogo or not os.path.isdir(self.pasta_jogo):
            messagebox.showerror("Erro", "A pasta do jogo não foi selecionada ou não existe.")
            return
        
        print(f"Tentando abrir o jogo em: {self.pasta_jogo} usando o executável: {self.jogo_executavel}")
        
        try:

            os.startfile(self.pasta_jogo)
            
            time.sleep(2) 
            
            pyautogui.write(os.path.basename(self.jogo_executavel))  
            pyautogui.press('enter')
            
            time.sleep(2)

            if not os.path.isfile('genesis_button.png'):
                messagebox.showerror("Erro", "A imagem do botão 'Genesis' não foi encontrada.")
                return

            genesis_button_location = pyautogui.locateOnScreen("genesis_button.png")
            
            if genesis_button_location:
                pyautogui.click(genesis_button_location)
                time.sleep(2)
                enter_game = pyautogui.locateOnScreen("enter_game.png", confidence=0.9)
                pyautogui.click(enter_game)
                time.sleep(7)
                pyautogui.click(x=1317, y=358)
            else:
                messagebox.showerror("Erro", "Botão 'Genesis' não encontrado na tela.")

            for conta in self.contas:
                threading.Thread(target=self.executar_bot, args=(conta['usuario'], conta['senha'])).start()
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar abrir o jogo: {str(e)}")
    
    def executar_bot(self, usuario, senha):
        self.realizar_login(usuario, senha)
    def realizar_login(self, usuario, senha):
        print (usuario)
        time.sleep(5) 
        pyautogui.typewrite(usuario)
        pyautogui.press('tab')
        time.sleep(1)  
        pyautogui.typewrite(senha)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter') 
        time.sleep(2)
        entergame2 = pyautogui.locateOnScreen("entergame2.png", confidence=0.9)
        pyautogui.click(entergame2) 

if __name__ == "__main__":
    root = tk.Tk()
    app = BotApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="123456",
            host="127.0.0.1",
            port="5432",
            database="controle_estoque"
        )
        return connection
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para consultar o banco de dados e exibir os resultados na Treeview
def consultar(treeview, codigo_material):
    try:
        connection = conectar_banco()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id, descricao, tipo, unidademed, quantidade FROM materiais"
            if codigo_material:
                query += f" WHERE id = '{codigo_material}'"
            cursor.execute(query)
            records = cursor.fetchall()
            for row in treeview.get_children():
                treeview.delete(row)
            for row in records:
                treeview.insert("", "end", values=row)
            cursor.close()
            connection.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao consultar o banco de dados: {e}")

 #
def consultar_desc(treeview, codigo_descr):
    try:
        connection = conectar_banco()
        if connection:
            cursor = connection.cursor()
            query = "SELECT id, descricao, tipo, unidademed, quantidade FROM materiais"
            if codigo_descr:
                query += f" WHERE descricao ILIKE '%{codigo_descr}%'"
            cursor.execute(query)
            records = cursor.fetchall()
            for row in treeview.get_children():
                treeview.delete(row)
            for row in records:
                treeview.insert("", "end", values=row)
            cursor.close()
            connection.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao consultar o banco de dados: {e}")       

# Função para abrir a janela de entrada de material
def entrada_material():
    def salvar_material():
        codigo = codigo_entry.get()
        descricao = descricao_entry.get()
        tipo = tipo_entry.get()
        unidade_medida = unidade_entry.get()
        quantidade = int(quantidade_entry.get())
        try:
            connection = conectar_banco()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT quantidade FROM materiais WHERE id = %s", (codigo,))
                record = cursor.fetchone()
                if record:
                    nova_quantidade = record[0] + quantidade
                    cursor.execute("UPDATE materiais SET quantidade = %s WHERE id = %s", (nova_quantidade, codigo))
                else:
                    cursor.execute(
                        "INSERT INTO materiais (id, descricao, tipo, unidademed, quantidade) VALUES (%s, %s, %s, %s, %s)",
                        (codigo, descricao, tipo, unidade_medida, quantidade)
                    )
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Sucesso", "Material inserido/atualizado com sucesso!")
                entrada_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir/atualizar material: {e}")

    entrada_window = tk.Toplevel()
    entrada_window.title("Entrada de Material")
    
    tk.Label(entrada_window, text="Código:").grid(row=0, column=0, padx=10, pady=5)
    codigo_entry = tk.Entry(entrada_window)
    codigo_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(entrada_window, text="Descrição:").grid(row=1, column=0, padx=10, pady=5)
    descricao_entry = tk.Entry(entrada_window)
    descricao_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(entrada_window, text="Tipo:").grid(row=2, column=0, padx=10, pady=5)
    tipo_entry = tk.Entry(entrada_window)
    tipo_entry.grid(row=2, column=1, padx=10, pady=5)
    
    tk.Label(entrada_window, text="Unidade de Medida:").grid(row=3, column=0, padx=10, pady=5)
    unidade_entry = tk.Entry(entrada_window)
    unidade_entry.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(entrada_window, text="Quantidade:").grid(row=4, column=0, padx=10, pady=5)
    quantidade_entry = tk.Entry(entrada_window)
    quantidade_entry.grid(row=4, column=1, padx=10, pady=5)
    
    tk.Button(entrada_window, text="Salvar", command=salvar_material).grid(row=5, column=0, columnspan=2, pady=10)

# Função para abrir a janela de saída de material
def saida_material():
    def salvar_saida():
        codigo = codigo_entry.get()
        quantidade = int(quantidade_entry.get())
        try:
            connection = conectar_banco()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT quantidade FROM materiais WHERE id = %s", (codigo,))
                record = cursor.fetchone()
                if record:
                    nova_quantidade = record[0] - quantidade
                    if nova_quantidade >= 0:
                        cursor.execute("UPDATE materiais SET quantidade = %s WHERE id = %s", (nova_quantidade, codigo))
                        connection.commit()
                        messagebox.showinfo("Sucesso", "Saída de material registrada com sucesso!")
                    else:
                        messagebox.showerror("Erro", "Quantidade insuficiente em estoque!")
                else:
                    messagebox.showerror("Erro", "Material não encontrado!")
                cursor.close()
                connection.close()
                saida_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar saída de material: {e}")

    saida_window = tk.Toplevel()
    saida_window.title("Saída de Material")
    
    tk.Label(saida_window, text="Código:").grid(row=0, column=0, padx=10, pady=5)
    codigo_entry = tk.Entry(saida_window)
    codigo_entry.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(saida_window, text="Quantidade:").grid(row=1, column=0, padx=10, pady=5)
    quantidade_entry = tk.Entry(saida_window)
    quantidade_entry.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(saida_window, text="Salvar", command=salvar_saida).grid(row=2, column=0, columnspan=2, pady=10)

# Função para criar a interface gráfica
def criar_interface():
    root = tk.Tk()
    root.title("Gerenciador de Estoque - Python")

    # Configuração da Treeview
    treeview = ttk.Treeview(root, columns=("id", "descricao", "tipo", "unidade_medida", "quantidade"), show="headings")
    treeview.heading("id", text="Código")
    treeview.heading("descricao", text="Descrição")
    treeview.heading("tipo", text="Tipo")
    treeview.heading("unidade_medida", text="Unidade de Medida")
    treeview.heading("quantidade", text="Quantidade")
    treeview.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

    # Frame para os botões e a caixa de pesquisa
    frame = tk.Frame(root)
    frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    # Caixa de pesquisa
    tk.Label(frame, text="Código do Material:").pack(padx=5, pady=5)
    codigo_entry = tk.Entry(frame)
    codigo_entry.pack(padx=5, pady=5)

    tk.Label(frame, text="Descrição do Material:").pack(padx=5, pady=5)
    codigo_desc = tk.Entry(frame)
    codigo_desc.pack(padx=5, pady=5)

    # Botão para consultar o banco de dados
    consultar_button = tk.Button(frame, text="Consultar", command=lambda: consultar(treeview, codigo_entry.get()))
    consultar_button.pack(fill=tk.X, padx=5, pady=5)

    consultardesc_button = tk.Button(frame, text="Consultar Descrição", command=lambda: consultar_desc(treeview, codigo_desc.get()))
    consultardesc_button.pack(fill=tk.X, padx=5, pady=5)

    # Botão para entrada de material
    entrada_button = tk.Button(frame, text="Entrada", command=entrada_material)
    entrada_button.pack(fill=tk.X, padx=5, pady=5)

    # Botão para saída de material
    saida_button = tk.Button(frame, text="Saída", command=saida_material)
    saida_button.pack(fill=tk.X, padx=5, pady=5)

    # Botão para sair da aplicação
    sair_button = tk.Button(frame, text="Sair", command=root.quit)
    sair_button.pack(fill=tk.X, padx=5, pady=5)

    root.mainloop()

# Chamada para iniciar a interface
criar_interface()

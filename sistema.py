import tkinter as tk
from tkinter import messagebox
import sqlite3

conexao = sqlite3.connect('produtos.db')
cursor = conexao.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS produto (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nome TEXT NOT NULL,
#     preco REAL NOT NULL,
#     descricao TEXT,
#     quantidade INTEGER NOT NULL,
#     codigo_barra TEXT UNIQUE
# )
# ''')

# cursor.execute('''
# ALTER TABLE produto ADD COLUMN codigo_barra TEXT UNIQUE;
# ''')
conexao.commit()


# Função para cadastrar produto
def cadastrar_produto():
    nome = entry_nome.get()
    preco = entry_preco.get()
    descricao = entry_descricao.get()
    quantidade = entry_quantidade.get()
    codigo_barra = entry_codigo_barra.get()

    if nome and preco and quantidade and codigo_barra:
        try:
            cursor.execute('''
            INSERT INTO produto (nome, preco, descricao, quantidade, codigo_barra)
            VALUES (?, ?, ?, ?, ?)
            ''', (nome, float(preco), descricao, int(quantidade), codigo_barra))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            limpar_campos()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Código de barras já existe!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {str(e)}")
    else:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")


# Função para consultar e exibir os produtos cadastrados
def consultar_produtos():
    cursor.execute('SELECT * FROM produto')
    produtos = cursor.fetchall()

    lista_produtos.delete(0, tk.END)  # Limpa a lista antes de adicionar novos itens
    for produto in produtos:
        lista_produtos.insert(tk.END,
                              f"ID: {produto[0]} | Nome: {produto[1]} | Preço: R${produto[2]} | Quantidade: {produto[4]} | Código de Barras: {produto[5]}")


# Função para buscar um produto pelo código de barras
def buscar_produto_por_codigo(event):
    codigo_barra = entry_codigo_barra.get()

    if codigo_barra:
        cursor.execute('SELECT * FROM produto WHERE codigo_barra = ?', (codigo_barra,))
        produto = cursor.fetchone()

        if produto:
            # Se o produto for encontrado, preencher os campos
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, produto[1])
            entry_preco.delete(0, tk.END)
            entry_preco.insert(0, produto[2])
            entry_descricao.delete(0, tk.END)
            entry_descricao.insert(0, produto[3])
            entry_quantidade.delete(0, tk.END)
            entry_quantidade.insert(0, produto[4])
        else:
            # Se não encontrar o produto, limpar os campos e permitir cadastro
            messagebox.showinfo("Produto não encontrado", "Produto não cadastrado. Insira os dados e cadastre.")
            limpar_campos()


# Função para limpar os campos após o cadastro
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_codigo_barra.delete(0, tk.END)


root = tk.Tk()
root.title("Cadastro de Produtos com Leitor de Código de Barras")

tk.Label(root, text="Código de Barras:").grid(row=0, column=0, padx=10, pady=10)
entry_codigo_barra = tk.Entry(root)
entry_codigo_barra.grid(row=0, column=1, padx=10, pady=10)
entry_codigo_barra.bind('<Return>', buscar_produto_por_codigo)  # Aciona a busca quando o código de barras é "bipado"

tk.Label(root, text="Nome do Produto:").grid(row=1, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Preço:").grid(row=2, column=0, padx=10, pady=10)
entry_preco = tk.Entry(root)
entry_preco.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Descrição:").grid(row=3, column=0, padx=10, pady=10)
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Quantidade:").grid(row=4, column=0, padx=10, pady=10)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=4, column=1, padx=10, pady=10)

btn_cadastrar = tk.Button(root, text="Cadastrar Produto", command=cadastrar_produto)
btn_cadastrar.grid(row=5, column=1, padx=10, pady=10)

btn_consultar = tk.Button(root, text="Consultar Produtos", command=consultar_produtos)
btn_consultar.grid(row=6, column=1, padx=10, pady=10)

lista_produtos = tk.Listbox(root, width=70)
lista_produtos.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

conexao.close()
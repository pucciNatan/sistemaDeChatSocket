import socket
import threading
from tkinter import *
from tkinter import simpledialog, messagebox

class Chat:
    def __init__(self):
        HOST = 'localhost'
        PORT = 55555
        
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cliente.connect((HOST, PORT))
        except socket.error as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            exit()

        login = Tk()
        login.withdraw()
        
        self.janela_carregada = False
        self.ativo = True

        # Coletar nome e sala com tratamento de erro
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)
        if not self.nome:
            messagebox.showerror("Erro", "Nome não pode ser vazio!")
            exit()

        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)
        if not self.sala:
            messagebox.showerror("Erro", "Sala não pode ser vazia!")
            exit()

        thread = threading.Thread(target=self.conecta)
        thread.start()
        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title('Chat')

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)
        
        self.envia_mensagem = Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.8, width=500, height=20)
        
        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
        
        self.root.mainloop()

    def fechar(self):
        self.ativo = False
        self.root.destroy()
        self.cliente.close()

    def conecta(self):
        while self.ativo:
            try:
                recebido = self.cliente.recv(1024)
                if not recebido:
                    messagebox.showwarning("Aviso", "Conexão encerrada pelo servidor.")
                    break
                if recebido == b'SALA':
                    self.cliente.send(self.sala.encode())
                    self.cliente.send(self.nome.encode())
                else:
                    self.caixa_texto.insert('end', recebido.decode() + '\n')
            except ConnectionAbortedError:
                break
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
                break

    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()
        if mensagem:  
            try:
                self.cliente.send(mensagem.encode())
                self.envia_mensagem.delete(0, 'end')
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível enviar a mensagem: {e}")

chat = Chat()

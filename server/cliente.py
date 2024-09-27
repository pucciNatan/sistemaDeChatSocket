import socket
import threading
from tkinter import *
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = 'localhost'
        PORT = 55555
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((HOST, PORT))
        login = Tk()
        login.withdraw()
        
        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)

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
        self.root.destroy()
        self.cliente.close()

    def conecta(self):
        while True:
            try:
                recebido = self.cliente.recv(1024)
                if recebido == b'SALA':
                    self.cliente.send(self.sala.encode())
                    self.cliente.send(self.nome.encode())
                else:
                    self.caixa_texto.insert('end', recebido.decode() + '\n')
            except ConnectionAbortedError:
                break
            except:
                pass

    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()
        if mensagem:
            self.cliente.send(mensagem.encode())
            self.envia_mensagem.delete(0, 'end')

chat = Chat()
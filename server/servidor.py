import socket
import threading

HOST = 'localhost'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

salas = {}

def broadcast(sala, mensagem):
    for cliente in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        try:
            cliente.send(mensagem)
        except:
            cliente.close()
            salas[sala].remove(cliente)

def enviarMensagem(nome, sala, cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem:
                print(f'{nome}: {mensagem}')
                broadcast(sala, f'{nome}: {mensagem}')
        except:
            cliente.close()
            salas[sala].remove(cliente)
            broadcast(sala, f'{nome} saiu da sala.')
            break

while True:
    cliente, addr = server.accept()
    cliente.send(b'SALA')
    sala = cliente.recv(1024).decode()
    nome = cliente.recv(1024).decode()

    if sala not in salas:
        salas[sala] = []
    salas[sala].append(cliente)
    print(f'{nome} se conectou na sala {sala}! INFO: {addr}')
    broadcast(sala, f'{nome} entrou na sala!')

    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, cliente))
    thread.start()
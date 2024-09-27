import socket
import threading

HOST = 'localhost'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((HOST, PORT))
    server.listen()
    print(f'Servidor escutando em {HOST}:{PORT}')
except Exception as e:
    print(f'Erro ao iniciar o servidor: {e}')
    exit(1)

salas = {}

def broadcast(sala, mensagem):
    if sala not in salas:
        return
    for cliente in salas[sala]:
        if isinstance(mensagem, str):
            mensagem = mensagem.encode()
        try:
            cliente.send(mensagem)
        except Exception as e:
            print(f'Erro ao enviar mensagem para {cliente}: {e}')
            try:
                cliente.close()
            except:
                pass
            salas[sala].remove(cliente)

def enviarMensagem(nome, sala, cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem:
                print(f'{nome}: {mensagem}')
                broadcast(sala, f'{nome}: {mensagem}')
            else:
                print(f'{nome} desconectou.')
                break
        except Exception as e:
            print(f'Erro ao receber mensagem de {nome}: {e}')
            break
    try:
        cliente.close()
        salas[sala].remove(cliente)
    except Exception as e:
        print(f'Erro ao fechar a conexão de {nome}: {e}')
    broadcast(sala, f'{nome} saiu da sala.')

while True:
    try:
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
    except Exception as e:
        print(f'Erro ao aceitar conexão: {e}')

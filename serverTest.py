import socket
import threading
import sys
import ssl
import json


def broadCastMensage(my_conn, my_addr, msg):
    len_msg = len(msg).to_bytes(2, "big")
    msg = len_msg + msg

    for conn in all_conn:
        if conn != my_conn:  # nao manda a msg para o proprio cliente que esta enviando
            try:
                conn.send(msg)
            except:
                print(f"falha no envio a {my_addr}")
                
def client(my_conn, my_addr):  # adrr ip e PORT conn = concexao atual
    print(f"Novo cliente conectado: {my_addr}")
    all_conn.append(my_conn)
    prefix = f"{my_addr} digitou: ".encode("utf-8")

    while True:
        try:
            len_msg = my_conn.recv(2)  # 2 bytes do tamanho
            len_msg = int.from_bytes(len_msg, "big")
            msg = prefix + my_conn.recv(len_msg)
            broadCastMensage(my_conn, my_addr, msg)
        except:
            print("Falha no processamento do cliente ", my_addr, "saindo.")
            break

    print(f"Cliente {my_addr} desconectado.")
    all_conn.remove(my_conn)
    my_conn.close()


HOST = "localhost"
PORT = 1234

all_threads = []
all_conn = []


def startServer():
    try:
        sock = socket.socket()  # flexibilidade de endereço
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # definida em socket e reutiliza PORTs ja conectadas (1 true)
        sock.bind((HOST, PORT))
        sock.listen()
        print("Aguardando conexões...")
    except OSError:
        print("Erro, endereço em uso.")  # tratamento para o erro de endereço do terminal
        sys.exit(2)
    return sock

def extract_json(response):
    try:
        return json.loads(response.split("\r\n\r\n", 1)[1])
    except (IndexError, json.JSONDecodeError):
        return {}

def receiverTelegramMsg():
    def wrapSocket(sock, serverurl):
        purpose = ssl.Purpose.SERVER_AUTH
        context = ssl.create_default_context(purpose)
        return context.wrap_socket(sock, server_hostname=serverurl)
    
    HOST = 'api.telegram.org'
    resource = '/bot6083297671:AAEx6pVBTfsLZ0-Kqq048eVqaLQKgi8sVW4'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, 443))
    sock = wrapSocket(sock, HOST)


    req = ('GET '+resource+'/getUpdates HTTP/1.1\r\n'+
           'Host: '+HOST+'\r\n'+
           '\r\n').encode()
    
    sock.sendall(req)
    
    resp = sock.recv(4096).decode()
    resp = extract_json(resp)
    resp = resp['result']
    
    for i in resp:
        print((f'{i['message']['from']['first_name']} DIGITOU: {i['message']['text']}'))


def main():
    sock = startServer()

    while True:
        try:
            conn, addr = sock.accept()
            t = threading.Thread(target=client, args=(conn, addr))  # config das all_threads
            
            
            all_threads.append(t)
            t.start()
        except Exception as e: 
            print(f"Erro no código:{e}")
            break

    for t in all_threads:
        t.join()  # recolhe os processors antes de fecha  sock.close()
        sock.close()

receiverTelegramMsg()
main()


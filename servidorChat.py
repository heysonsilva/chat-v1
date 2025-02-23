import socket
import threading
import sys
import ssl
import json
import time

def broadCastMensage(my_conn, my_addr, msg):
    len_msg = len(msg).to_bytes(2, "big")
    msg = len_msg + msg

    for conn in all_conn:
        if my_conn == None or conn != my_conn:  # nao manda a msg para o proprio cliente que esta enviando e agora Garante que mensagens do Telegram sejam enviadas
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
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(5)
        print("Aguardando conexões...")
    except OSError:
        print("Erro, endereço em uso.")
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
    last_update_id = None  # Guarda o últmo update_id processado

    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, 443))
        sock = wrapSocket(sock, HOST)

        req = ('GET ' + resource + '/getUpdates HTTP/1.1\r\n' +
               'Host: ' + HOST + '\r\n' +
               '\r\n').encode()
        
        sock.sendall(req)
        res = sock.recv(4096).decode()
        res = extract_json(res)
        res = res.get("result", [])
        

        for msg_data in res:
            update_id = msg_data["update_id"]
            if last_update_id is None or update_id > last_update_id:
                last_update_id = update_id  # Atualiza o último update_id
                first_name = msg_data["message"]["from"]["first_name"]
                text = msg_data["message"]["text"]
                formatted_msg = f"[TELEGRAM] {first_name}: {text}".encode("utf-8")
                print(f"Recebida do Telegram: {first_name}: {text}")
                broadCastMensage(None, "TELEGRAM", formatted_msg)

        time.sleep(10)  # Aguarda 10 segundo para mandar novamente a requisiçap 




def main():
    sock = startServer()
    threading.Thread(target=receiverTelegramMsg, daemon=True).start()

    while True:
        try:
            conn, addr = sock.accept()
            t = threading.Thread(target=client, args=(conn, addr))
            
            all_threads.append(t)
            t.start()
        except Exception as e: 
            print(f"Erro no código:{e}")
            break

    for t in all_threads:
        t.join()
        sock.close()

main()

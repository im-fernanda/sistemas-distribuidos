import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                print("\nMensagem recebida:", msg)
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    print("Você pode começar a digitar suas mensagens.")
    while True:
        msg = input("> ")
        if msg.lower() == "sair":
            break
        client.send(msg.encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()
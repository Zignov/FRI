import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)
import socket
import struct
import threading
import json

PORT = 8888
HEADER_LENGTH = 2
usernames = {}


def receive_fixed_length_msg(sock, msglen):
    message = b''
    while len(message) < msglen:
        chunk = sock.recv(msglen - len(message))  # preberi nekaj bajtov
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        message = message + chunk  # pripni prebrane bajte sporocilu

    return message


def receive_message(sock):
    header = receive_fixed_length_msg(sock,
                                      HEADER_LENGTH)  # preberi glavo sporocila (v prvih 2 bytih je dolzina sporocila)
    message_length = struct.unpack("!H", header)[0]  # pretvori dolzino sporocila v int

    message = None
    if message_length > 0:  # ce je vse OK
        message = receive_fixed_length_msg(sock, message_length)  # preberi sporocilo
        message = message.decode("utf-8")

    return message


def send_message(sock, message):
    encoded_message = message.encode("utf-8")  # pretvori sporocilo v niz bajtov, uporabi UTF-8 kodno tabelo

    # ustvari glavo v prvih 2 bytih je dolzina sporocila (HEADER_LENGTH)
    # metoda pack "!H" : !=network byte order, H=unsigned short
    header = struct.pack("!H", len(encoded_message))

    message = header + encoded_message  # najprj posljemo dolzino sporocilo, slee nato sporocilo samo
    sock.sendall(message);


# funkcija za komunikacijo z odjemalcem (tece v loceni niti za vsakega odjemalca)
def client_thread(client_sock, client_addr):
    global clients

    print("[system] connected with " + client_addr[0] + ":" + str(client_addr[1]))
    print("[system] we now have " + str(len(clients)) + " clients")

    try:

        while True:  # neskoncna zanka
            msg_received = receive_message(client_sock)

            if not msg_received:  # ce obstaja sporocilo
                break

            print(f"[RKchat] [{client_addr[0]}:{client_addr[1]}] : {msg_received}")

            try:
                msg_obj = json.loads(msg_received)
                msg_type = msg_obj.get("type", "public")
                sender_name = msg_obj.get("from", "Unknown")

                # shrani uporabniško ime, če še ni
                if client_sock not in usernames:
                    usernames[client_sock] = sender_name

                response = {
                    "type": msg_type,
                    "from": sender_name,
                    "timestamp": msg_obj.get("timestamp", ""),
                    "message": msg_obj.get("message", "")
                }

                if msg_type == "private":
                    recipient_name = msg_obj.get("to")
                    with clients_lock:
                        for client in clients:
                            if usernames.get(client) == recipient_name:
                                send_message(client, json.dumps(response))
                                break
                else:
                    # pošlji vsem razen pošiljatelju
                    with clients_lock:
                        for client in clients:
                            if client != client_sock:
                                send_message(client, json.dumps(response))

            except json.JSONDecodeError:
                continue

    except Exception as e:
        print(f"[napaka] {e}")
    finally:
        with clients_lock:
            clients.remove(client_sock)
            if client_sock in usernames:
                del usernames[client_sock]
        print("[system] prekinjena povezava z " + client_addr[0] + ":" + str(client_addr[1]))
        print("[system] trenutno povezanih: " + str(len(clients)))
        client_sock.close()

# kreiraj socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", PORT))
server_socket.listen(1)

# cakaj na nove odjemalce
print("[system] listening ...")
clients = set()
clients_lock = threading.Lock()


while True:
    try:
        # pocakaj na novo povezavo - blokirajoc klic
        client_sock, client_addr = server_socket.accept()
        with clients_lock:
            clients.add(client_sock)

        thread = threading.Thread(target=client_thread, args=(client_sock, client_addr));
        thread.daemon = True
        thread.start()

    except KeyboardInterrupt:
        break

print("[system] closing server socket ...")
server_socket.close()

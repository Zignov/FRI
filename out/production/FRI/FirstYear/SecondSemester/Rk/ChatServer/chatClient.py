import socket
import struct
import sys
import threading
import datetime
import json

PORT = 8888
HEADER_LENGTH = 2


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


# message_receiver funkcija tece v loceni niti
def message_receiver():
    while True:
        try:
            msg_received = receive_message(sock)
            msg_object = json.loads(msg_received)
            if len(msg_received) > 0:  # ce obstaja sporocilo
                msg_type = msg_object.get("type")
                sender = msg_object.get("from", "Unknown")
                timestamp = msg_object.get("timestamp")
                message = msg_object.get("message", "")

                # Handle the message format
                if msg_type == "private":
                    print(f"[{timestamp}] {sender}: {message}")
                else:
                    print(f"[{timestamp}] {sender}: {message}")
        except:
            continue

# uporabnik mora vpisati svoje ime
ime = input("Vnesite ime ")


# povezi se na streznik
print("[system] connecting to chat server ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", PORT))
print("[system] connected!")

#poslji pozravljen
sporociloObj = {
    "type": "public",
    "from": ime,
    "timestamp": datetime.datetime.now().strftime("%H:%M"),
    "message": f"uporabnik {ime} se je povezal"
}
send_message(sock, json.dumps(sporociloObj))

# zazeni message_receiver funkcijo v loceni niti
thread = threading.Thread(target=message_receiver)
thread.daemon = True
thread.start()

# pocakaj da uporabnik nekaj natipka in poslji na streznik
while True:
    try:

        msg_send = input()
        time = datetime.datetime.now().strftime("%H:%M")

        if msg_send.startswith("/msg"):
            deli = msg_send.split(" ", 2)

            if len(deli) >= 3:
                prejemnik = deli[1]
                sporocilo = deli[2]

                sporociloObj = {
                    "type": "private",
                    "from": ime,
                    "to": prejemnik,
                    "timestamp": time,
                    "message": sporocilo
                }


        else:


            sporociloObj = {
                    "type": "public",
                    "from": ime,
                    "timestamp": time,
                    "message": msg_send
                }
            

        send_message(sock, json.dumps(sporociloObj))
            
    except KeyboardInterrupt:
        sys.exit()

from Crypto.Cipher import AES
import socket
from networkinformationfunctions import *

nonce = b'\xc3A\x85\xdc'
ctr = {'counter_len': 8, 'prefix': b'\xc3A\x85\xdc', 'suffix': b'ABCD', 'initial_value': 10, 'little_endian': True}
key = b'\xb7\xd3b\x90\xc5\xa0f\x9f\\\xce\x19\x0f}j\x04\x08\xfatQ\xf3R@\xae\xf8=\x80\xa1&\xa7f\xd0\n'
#nonce = Random.get_random_bytes(4)
#ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
#key = os.urandom(32)




def do_encrypt(message): # function that encrypts the message
    encrypto = AES.new(key, AES.MODE_CTR, counter=ctr)
    return encrypto.encrypt(message)
def do_decrypt(message): # function that decrypts the message
    decrypto = AES.new(key, AES.MODE_CTR, counter=ctr)
    return decrypto.decrypt(message)

def connectClient():     # creates a client connection with a server that sends an encrypted message
    print("WARNING! In order to close an established connection an exit message must be sent across the tcp tunnel.")
    print("To close the connection type 'exit' as your final message.")
    host = checkHostName("")
    port = input("Which tcp port would you like to use? (Default Port: 8080) ")
    if port == '':
        port = 8080
    else:
        port = int(port)
    message = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except:
        input("An error occurred and a connection could not be established. Hit enter to return to the options menu....")
        return
    while 'exit' not in message.lower():
        message = input("What message would you like to send over the TCP tunnel? ")
        ciphermsg = do_encrypt(message.encode('utf-8'))
        try:
            s.sendall(ciphermsg)
            print("Sent the message....")
            while True:
                data = s.recv(1024)
                if data:
                    plaintext = do_decrypt(data)
                    print('Received Acknowledgement from Server:', plaintext.decode())
                    break
                else:
                    print('no data received')
        except:
            print("An error occurred and a connection could not be established. Returning to the options menu....")
            s.close()
            print("Connection closed.")
            return
    s.close()
    print("Connection closed.")
    return



def connectServer():  # creates a server connection with a client that receives encrypted messages
    try:
        host = '' #localhost
        port = input("Which tcp port would you like to use? (Default Port: 8080) ")
        if port == '':
            port = 8080
        else:
            port = int(port)
        timeOutValue = input("How long (in seconds) until the socket times out and closes the connection? (Default is 10 seconds) ")
        if timeOutValue == '':
            timeOutValue = 10
        else:
            timeOutValue = int(timeOutValue)
        socket.setdefaulttimeout(timeOutValue)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        print('[+] Listening for incoming TCP connection on port', str(port))
        conn, addr = s.accept()
        print(addr, "is connected")
    except:
        input("Error: Connection in use or Timed Out. Hit ENTER to return to the options menu.")
        return

    try:
        plaintext = ""
        while True:
            data = conn.recv(1024)
            plaintext = do_decrypt(data).decode()
            print("Received Secure Message from Client:", plaintext)
            print("Sending an acknowledgement...")
            if 'exit' in plaintext.lower():
                acknowledge = do_encrypt("Last MSG received, now closing connection.".encode('utf-8'))
                conn.sendall(acknowledge)
                print("Closing connection")
                conn.close()
                s.close()
                break

            acknowledge = do_encrypt("MSG Received".encode('utf-8'))
            conn.sendall(acknowledge)
            print("Listening for next message...")
    except socket.error:
        print("Error Occurred...")
        input("Connection may have timed out. Hit ENTER to return to the options menu.")
        return

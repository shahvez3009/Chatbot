import socket, threading, time, argparse
# TCP server
# parser that checks if necessary arguments are provided
argParser = argparse.ArgumentParser(description='Start server.Example: server.py 7070')
argParser.add_argument('port', type=int, help='Write the port for the server. most after 4000 are available')

port = argParser.parse_args().port

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Made a socket, with socket family and streaming data through the socket.
serverSocket.bind(('localhost', port)) #Binding socket to localhost and the specific port.
serverSocket.listen()  # Socket will listen for conncetions


clients = []  # clients listed here
usernames = []  # client names listed here


# This functions handles the communication between bots and hots
def handle(client):
    while True:
        try:
            messageReceived = client.recv(1024) # Receiving message from client
            time.sleep(2)
            messageToEveryone(client, messageReceived)  # send the message to everyone else

        except:
            tmp = clients.index(client)
            clients.remove(client) #Removes client from list
            client.close()
            name = usernames[tmp]
            print(f'{name} has left the server') #Print message to server terminal
            usernames.remove(name) #Removes name from the list
            break

#Sends message to eveyone
def messageToEveryone(client, message):
    for user in clients:
        if user is not client: #Makes sure that the message does not get sent back to the original sender
            user.send(message)


def start():
    print('Server is running and listening for connections') #Print to server terminal
    while True:
        client, address = serverSocket.accept()  # accepts all connections

        client.send('usernames'.encode('utf-8')) #Send message about username, to get them
        newUser = client.recv(1024).decode('utf-8') #Decode the information about new uer
        clients.append(client) #Add to list
        usernames.append(newUser) #Add to list
        print(f'{newUser} has a connection to the server') #prints to the server terminal
        messageToEveryone(client, f'{newUser} has connected to the chat room'.encode('utf-8')) #Informs everyone that a new user has entered
        #Makes it possible to connect to multiple bots
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


start()

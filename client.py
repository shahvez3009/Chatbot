
import socket, random, threading, sys, time, argparse
# TCP client
#Parser for arguments required
argParser = argparse.ArgumentParser(description=' Example: client.py shahvez localhost 4242 ')
argParser.add_argument('name', type=str, help='The name for host or bot. Connect as a host or Shahvez, Ali or Emma') # This is to check name is provided
argParser.add_argument('host', type=str, help='Address of the server connecting to.') #This is to check if host is provided
argParser.add_argument('port', type=int, help='Port to connect, most after 4000 are available') #This is to check if a port is provided and in integer

#Using the arguemnts provided as variables
host = argParser.parse_args().host
port = argParser.parse_args().port
name = argParser.parse_args().name

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Made a socket, with socket family and streaming data through the socket.
clientSocket.connect((host, port))


# Two different list, one for positive actions and one for negative
positiveVerbs = ["swim", "run", "jog", "eat", "cycle", "skateboard", "work", "dance"]
negativeVerbs = ["smoke", "rob", "attack", "hike", "destroy", "bully"]

chatBots = ["shahvez", "ali", "emma"] #List for the names of the bots

print("You have entered the chat room") # Welcome message in the chat room

# the bot functions,the bots have the same format of code and therefore just inline comments on the first function
def shahvez(action):
    if action in positiveVerbs: #Checks if the suggested action is positive
        posAnswer = [
            f"{name}: You want us to {action}? Me too! \n",
            f"{name}: To {action} that sounds amazing! \n",
            f"{name}: I cannot wait to {action}! \n"
        ]
        return random.choice(posAnswer) # Returns back a random positive action

    elif action in negativeVerbs:  #Checks if the suggested action is negative
        negativeAnswers = [
            f"{name}: I dont want to {action} \n",
            f"{name}: I do not like to {action} \n",
            f"{name}: I am afraid to {action} \n"
        ]
        return random.choice(negativeAnswers) # Returns back a random positive action

    else:
        # If the suggested action is not in the action lists, the bot will suggest to do something else
        return f"{name}:  Could we do something else please \n"


def ali(action):
    if action in positiveVerbs:
        posAnswer = [
            f"{name}: Yes! {action} Lets do it! \n",
            f"{name}: What are we waiting for! Lets {action} \n",
            f"{name}: Yes, I would like that \n"
    ]
        return random.choice(posAnswer)

    elif action in negativeVerbs:
        negativeAnswer = [
            f"{name}:Something else than to {action} \n",
            f"{name}: I do not like to {action} \n",
            f"{name}: {action}? I object! \n"
        ]
        return random.choice(negativeAnswer)

    else:
        return f"{name}: I am uninterested \n"


def emma(action):
    if action in positiveVerbs:
        posAnswers = [
            f"{name}: Yes! {action}? Lets meet now! \n",
            f"{name}: To {action}, first time for me! \n",
            f"{name}: I am excited to {action} \n"
        ]
        return random.choice(posAnswers)

    elif action in negativeVerbs:
        negativeAnswer = [
            f"{name}: Another activity would be nice \n",
            f"{name}:  I have a phobia to {action} \n",
            f"{name}: {action}? I cannot I am afraid! \n"
        ]
        return random.choice(negativeAnswer)

    else:
        return f"{name}: What about another idea? Because that is boring "



def receive():
    while True:
        msg = clientSocket.recv(1024).decode('utf-8') #Decodes the message recieved from the server

        if msg == "usernames":
            clientSocket.send(name.encode('utf-8')) #Send the name of the new user that connected

        else:
            if ":" in msg:

                msgSplit = msg.split(": ") #Splits the message to get the name separate
                botCheck = msgSplit[0] #Saves the name of the messager

                if botCheck not in chatBots: #Checks if the messager is a bot
                    action = "" #Variable to save the suggested action in the message recieved

                    for word in positiveVerbs:
                        if word in msg: #Checks if there are any of the positive verbs in the message
                            action = word #Assigns the positive word to a variable, if there is any

                    for word in negativeVerbs:
                        if word in msg:  #Checks if there are any of the negative verbs in the message
                            action = word #Assigns the negative word to a variable, if there is any

                    if name == "shahvez":
                        send(shahvez(action))

                    elif name == "ali":
                        send(ali(action))

                    elif name == "emma":
                        send(emma(action))

                    print(msg)

                else: #To recieve the answer from the bots
                    time.sleep(1.5)
                    print(msg)

            else: #prints that host has entered the chat to the others
                print(msg)


def send(msg):
    print(msg)
    clientSocket.send(msg.encode('utf-8'))


# Sends the host message
def message():
    while True:
        try:
            msg = f'{name}: {input()}' #Formats the message
            time.sleep(1)
            clientSocket.send(msg.encode('utf-8'))
        except:
            sys.exit()

#Both these threads makes it possible to listen and writing to everyone
receive_thread = threading.Thread(target=receive)
receive_thread.start()

if name not in chatBots:
    send_thread = threading.Thread(target=message)
    send_thread.start()

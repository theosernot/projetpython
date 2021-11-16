#!/ usr/ bin/ python3

import select
import socket
s = socket . socket ( socket . AF_INET6 , socket . SOCK_STREAM , 0)
s. setsockopt ( socket . SOL_SOCKET , socket . SO_REUSEADDR , 1)
s. bind (("", 9000) )
s. listen (1)
l = []
m = []
o = 0
j = []
dict = {}
dict2 = {}
dict3 = {}
while True :
    c,b,n = select.select(l+[s],[],[])
    for i in c:

#Ajout de nouveaux utilisateurs
        if i == s:
            sc , a = s.accept()
            print("new client :", a)
            l.append(sc)
            m.append(sc.getpeername())
            o+=1
            ip=str(m[o-1][0])
            port=str(m[o-1][1])
            new = ("User " + "<" + ip + ">" + ":" + "<" + port + ">" + " connected\n")
            dict2[str(port)] = sc
            for k in l:
                if k != sc:
                    k.send(new.encode("utf-8"))

#Envoie des messages / commandes
        else:
            msg = i.recv (1500)
            msg2 = msg.decode("utf-8")
            if msg2[0:5] == "NICK ":
                nick = msg2[5:]
                h = i.getpeername()
                port = h[1]
                dict[str(port)] = str(nick.strip())
                dict3[str(nick.strip())] = str(port)

#Commande pour envoyer un message
            elif msg2[0:4] == "MSG ":
                h = i.getpeername()
                port = h[1]
                for k in l:
                    if k != i:
                        x = str([dict.get(str(port))]) + ":"
                        msg3 = x + " " + msg2[4:]
                        k.send(msg3.encode("utf-8"))

#Liste des utilisateurs sur le serveur 
            elif msg2[0:3] == "WHO":
                for gertrude in dict.values():
                    h = gertrude + "\n"
                    for k in l:
                        if k == i:
                            k.send(h.encode("utf-8"))

#Commande pour se déconnecter
            elif msg2[0:5] == "QUIT ":
                for k in l:
                    if k != i:
                        msg3 = msg2[5:]
                        k.send(msg3.encode("utf-8"))
                l.remove(i)
                i.close()

#Exclusion d'un utilisateur
            elif msg2[0:5] == "KILL ":
                print(msg2[5:].strip())
                print(dict3)
                h = dict3.get(msg2[5:].strip())
                h2 = dict2.get(h)
                h2.close()
                l.remove(h2)
                

                # l.remove(h2)
                # h2.close()

#Déconnexion d'un utilisateur
            elif len(msg) == 0:
                print (" client disconnected ")
                h = i.getpeername()
                port = h[1]
                left=("User " + str(dict.get(str(port))) + " disconnected\n")
                l.remove(i)
                i.close()
                for k in l:
                    k.sendall(left.encode("utf-8")) 
                break
            else:
                err="Invalid Command \n"
                i.send(err.encode("utf-8"))
s.close()


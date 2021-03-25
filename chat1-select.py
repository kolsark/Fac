#!/usr/bin/python3
import socket
import select


HOST = ""
PORT = 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                # Création et paramétrage du socket serveur.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                              # 
s.bind((HOST, PORT))                                                                                 # Création des Listes servant de base de données : 
s.listen(1)                                                                                          # - l contient les duos ip:port.
l = []                                                                                               # - lNick contient les pseudos choisis (ip:port par défaut).
lNick = []                                                                                           # l[x] contient l'ip et le port du client x, et lNick[x] contient le pseudo du client x.
                                                                                                     # La clé utilisée est donc l'indice dans l correspondant au client.
while True:
    lr, _, _ = select.select(l + [s], [], [])                                                        # Déroulement de la boucle bloquée en attendant la réception d'un paquet TCP client.
     
    for i in lr:                                            
        if(i == s):                                                                                  # Si le paquet correspond à l'arrivée d'un nouveau client :
            sclient, printClient = s.accept()                         
            print("Nouveau client connecté :", printClient)                                          # - Affichage d'un msg sur le serveur
            msgBeginConnexion = "Nouveau client connecté ! :% s" % sclient.getpeername()[0] + ":" + "% s" % sclient.getpeername()[1] + "\n" 
            for j in l:                                                                              # - Envoi d'une notif de connection aux autres clients.
                if j != i and j != s:
                    j.sendall(msgBeginConnexion.encode("utf-8"))
            l.append(sclient)                                                                        # - Enregistrement à l'emplacement x dans l et dans lNick de son ip et son port.
            lNick.append("% s" % sclient.getpeername()[0] + ":" + "% s" % sclient.getpeername()[1])
            print(lNick)
            
        else:                                                                                        # Si le client emetteur n'est pas un nouveau client :
            data = i.recv(1500).decode()                                                             # On récupère les données du paquet pour les "disséquer" puis les traiter.
            print(data)
            
            if(data == "" or data == "\n"):                                                          # Si le msg est vide, on affiche sur le serveur et sur les clients une notif de déconnexion 
                msgCloseConnexion = "Client déconnecté ! : " + "% s \n" % lNick[l.index(i)]
                
                for j in l:
                    if j != i and j != s:
                        j.sendall(msgCloseConnexion.encode("utf-8"))
                        
                i.close()
                print("client déconnecté")
                
                del lNick[l.index(i)]                                                               # Puis on retire le client déconnecté des Listes servant à stocker les infos de clients.
                l.remove(i)
                continue
            
            if(data.split(maxsplit=1)[0] == "MSG" and len(data.split(maxsplit=1)[1]) > 0):          # Si la première partie du paquets == "MSG", on a affaire à un msg,
                txtMsg = "[" + "% s" % lNick[l.index(i)] + "] " + "% s" % data.split(maxsplit=1)[1] # on le transmet simplement en brut à tous les autres clients.
                for j in l:        
                    if j != i:                                                                      
                        j.sendall(txtMsg.encode("utf-8"))
                continue
                        
            if(data.split(maxsplit=1)[0] == "NICK" and len(data.split(maxsplit=1)[1]) > 0):        # Si la première partie == "NICK", c'est une demande de changement de pseudo,
                lNick[l.index(i)] = data.split(maxsplit=1)[1].split('\n',maxsplit=1)[0]            # on modifie lNick[x], avec x étant le client émetteur, et on remplace l'entrée par la
                print(lNick)                                                                       # deuxième partie du paquet.
                continue
            
            if(data == "WHO\n"):                                                                   # Si la première partie du paquet == "WHO", on envoie lNick au client émetteur.
                listeClients = ""
                for b in lNick:
                    listeClients += "% s " % b
                listeClients += "\n"
                i.sendall(listeClients.encode("utf-8"))
                continue
                
            if(data.split(maxsplit=1)[0] == "QUIT"):                                               # Si la première partie du paquet == "QUIT", on transmet la 3e partie du paquet (le msg à afficher)
                txtAdieu = "[" + "% s" % lNick[l.index(i)] + "] " + "% s" % data.split(maxsplit=1)[1]
                for j in l:                                                                        # au serveur et aux clients, puis on ferme le socket du client émetteur.
                    if j != i:             
                        j.sendall(txtAdieu.encode("utf-8"))
                i.close()
                print("client déconnecté")
                
                del lNick[l.index(i)]                                                              # On retire le clients déconnecté des listes l et lNick
                l.remove(i)
                continue
            
            if(data.split(maxsplit=2)[0] == "KILL"):                                               # Si la première partie du paquet == "KILL", on transmet la 3e partie du paquet (le msg à afficher)
                txtKill = "[" + "% s" % lNick[l.index(i)] + "] " + "% s" % data.split(maxsplit=2)[2]
                sockToKill = l[lNick.index(data.split(maxsplit=2)[1])]                             # au client dont le pseudo == la 2e partie du paquet.
                sockToKill.sendall(txtKill.encode("utf-8"))
                
                sockToKill.close()                                                                 # Puis on ferme son socket ...
                print("client déconnecté")
                
                del lNick[l.index(sockToKill)]                                                     # ... et on le retire des listes l et lNick
                l.remove(sockToKill)
                continue
                
            
            else:
                ErrMsg = "Invalid command!\n"                                                      # Si le contenu de data n'est pas géré par le programme (commande inconnue...)
                i.sendall(ErrMsg.encode("utf-8"))                                                  # ou si il y a une erreur de frappe, envoi d'un msg d'erreur.
                
                                                                                                   # On retourne au début du While
s.close()
import socket
import ssl

# Configuration de la cible
hote = "zeldawikidelinkrob.fandom.com"
# Chemin de l'API cachée de MediaWiki pour lister les pages
chemin = "/api.php?action=query&list=allpages&format=json"

print(f"[*] Connexion sécurisée à {hote}...")

# 1. Création d'une connexion SSL/TLS sécurisée (Port 443 comme vu au scan)
contexte = ssl.create_default_context()
with socket.create_connection((hote, 443)) as sock:
    with contexte.wrap_socket(sock, server_hostname=hote) as ssock:
        
        # 2. Construction de la requête HTTP brute (comme un vrai navigateur)
        requete = (
            f"GET {chemin} HTTP/1.1\r\n"
            f"Host: {hote}\r\n"
            "User-Agent: CyberScanner/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
        
        # 3. Envoi de la requête au serveur de ton wiki
        ssock.sendall(requete.encode())
        
        # 4. Récupération de la réponse du serveur
        reponse = b""
        while True:
            donnees = ssock.recv(4096)
            if not donnees:
                break
            reponse += donnees

# 5. Décodage et affichage du résultat brut informatique (JSON)
print("[+] Données du wiki récupérées avec succès :\n")
print(reponse.decode(errors='ignore'))

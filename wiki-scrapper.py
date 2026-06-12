import socket
import ssl
import urllib.parse

print("=== EXTRACTEUR DE CONTENU DE WIKI ===")
hote = "zeldawikidelinkrob.fandom.com"

# On demande à l'utilisateur quelle page il veut aspirer
page_cible = input("Entrez le titre de la page à extraire (ex: Appareil Photo, Arbre Mojo) : ")

# Étape cruciale : On encode le titre pour que les espaces et accents passent dans l'URL
page_encodee = urllib.parse.quote(page_cible)

# Chemin de l'API pour récupérer le TEXTE BRUT de l'article spécifié
chemin = f"/api.php?action=query&titles={page_encodee}&prop=revisions&rvprop=content&format=json"

print(f"[*] Extraction du contenu de la page '{page_cible}'...")

contexte = ssl.create_default_context()
with socket.create_connection((hote, 443)) as sock:
    with contexte.wrap_socket(sock, server_hostname=hote) as ssock:
        
        requete = (
            f"GET {chemin} HTTP/1.1\r\n"
            f"Host: {hote}\r\n"
            "User-Agent: CyberScanner/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
        
        ssock.sendall(requete.encode())
        
        reponse = b""
        while True:
            donnees = ssock.recv(4096)
            if not donnees:
                break
            reponse += donnees

# On sépare l'en-tête HTTP du vrai contenu JSON pour y voir plus clair
parties = reponse.decode(errors='ignore').split("\r\n\r\n")
corps_json = parties[1] if len(parties) > 1 else reponse.decode(errors='ignore')

print("[+] Contenu brut récupéré :\n")
print(corps_json)

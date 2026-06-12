import socket
import ssl
import urllib.parse
import json
import os

print("=== DEVOPS WIKI MINER & CLEANER ===")
hote = "zeldawikidelinkrob.fandom.com"

page_cible = input("Entrez le titre de la page à aspirer (ex: Appareil Photo) : ")
page_encodee = urllib.parse.quote(page_cible)

chemin = f"/api.php?action=query&titles={page_encodee}&prop=revisions&rvprop=content&format=json"

print(f"[*] Aspiration de la page '{page_cible}'...")

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

# --- ÉTAPE 1 : ISOLEMENT ET NETTOYAGE JSON ---
parties = reponse.decode(errors='ignore').split("\r\n\r\n")
corps_json = parties[1] if len(parties) > 1 else parties[0]

try:
    donnees_ordonnees = json.loads(corps_json)
    pages = donnees_ordonnees["query"]["pages"]
    page_id = list(pages.keys())[0]
    
    if page_id == "-1":
        print("[-] Erreur : Cet article n'existe pas sur ton wiki.")
        exit(1)
        
    # Extraction du texte brut de l'article (sans les codes Unicode \u00e9 bizarres)
    texte_propre = pages[page_id]["revisions"][0]["*"]
    
    print("\n[+] CONTENU NETTOYÉ DE L'ARTICLE :")
    print("-" * 40)
    print(texte_propre)
    print("-" * 40)

    # --- ÉTAPE 2 : SAUVEGARDE AUTOMATIQUE EN .TXT ---
    # On remplace les espaces par des tirets pour faire un nom de fichier propre
    nom_fichier = f"{page_cible.replace(' ', '_')}.txt"
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"ARTICLE ASPIRÉ : {page_cible}\n")
        f.write("=" * 30 + "\n\n")
        f.write(texte_propre)
        
    print(f"[+] Succès : Fichier local créé ➔ {nom_fichier}")

except Exception as e:
    print(f"[-] Erreur lors du nettoyage des données : {e}")

import socket
import ssl
import json
import urllib.parse
import time

hote = "zeldawikidelinkrob.fandom.com"
contexte = ssl.create_default_context()

def envoyer_requete(chemin_api):
    """Fonction réutilisable pour interroger l'API en HTTPS brut"""
    with socket.create_connection((hote, 443)) as sock:
        with contexte.wrap_socket(sock, server_hostname=hote) as ssock:
            requete = (
                f"GET {chemin_api} HTTP/1.1\r\n"
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
    parties = reponse.decode(errors='ignore').split("\r\n\r\n")
    return parties[1] if len(parties) > 1 else parties[0]

print("=== DEVOPS MASS WIKI ASPIRATOR ===")
print("[*] Étape 1 : Récupération de la liste de TOUS les articles...")

chemin_liste = "/api.php?action=query&list=allpages&aplimit=max&format=json"
corps_liste = envoyer_requete(chemin_liste)

try:
    donnees_liste = json.loads(corps_liste)
    liste_pages = donnees_liste["query"]["allpages"]
    titres = [page["title"] for page in liste_pages]
    
    print(f"[+] {len(titres)} articles détectés sur le wiki :")
    print(", ".join(titres))
    print("\n[*] Étape 2 : Aspiration de masse en cours...")

    for titre in titres:
        print(f" -> Téléchargement et nettoyage de : {titre}...")
        titre_encode = urllib.parse.quote(titre)
        chemin_article = f"/api.php?action=query&titles={titre_encode}&prop=revisions&rvprop=content&format=json"
        
        corps_article = envoyer_requete(chemin_article)
        donnees_article = json.loads(corps_article)
        pages = donnees_article["query"]["pages"]
        page_id = list(pages.keys())[0]
        
        if page_id != "-1":
            texte_propre = pages[page_id]["revisions"][0]["*"]
            nom_fichier = f"{titre.replace(' ', '_').replace('/', '_')}.txt"
            with open(nom_fichier, "w", encoding="utf-8") as f:
                f.write(f"ARTICLE : {titre}\n")
                f.write("=" * 30 + "\n\n")
                f.write(texte_propre)
        
        time.sleep(0.2)

    print("\n[++] TOUS LES ARTICLES ONT ÉTÉ ASPIRÉS ET SAUVEGARDÉS !")

except Exception as e:
    print(f"[-] Erreur durant l'aspiration globale : {e}")

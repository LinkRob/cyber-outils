import urllib.request
import urllib.parse
import json
import time
import os

print("=== DEVOPS FANDOM INJECTOR (COMPLETE) ===")

hote = "zeldawikidelinkrob.fandom.com"
username = "LinkRob"
password = "LinkRob est le meilleur au monde"

def envoyer_requete_fandom(chemin_api, donnees_post=None, cookies=None):
    url = f"https://{hote}{chemin_api}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DevOpsInjector/2.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    if cookies:
        headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        
    donnees_encodees = urllib.parse.urlencode(donnees_post).encode('utf-8') if donnees_post else None
    
    try:
        req = urllib.request.Request(url, data=donnees_encodees, headers=headers, method="POST" if donnees_post else "GET")
        with urllib.request.urlopen(req, timeout=12) as r:
            set_cookie = r.info().get_all('Set-Cookie')
            nouveaux_cookies = {}
            if set_cookie:
                for c in set_cookie:
                    if "=" in c:
                        crumbs = c.split(';')[0].split('=')
                        if len(crumbs) >= 2:
                            nouveaux_cookies[crumbs[0].strip()] = crumbs[1].strip()
            
            return json.loads(r.read().decode('utf-8')), nouveaux_cookies
    except Exception as e:
        print(f"[-] Erreur réseau/API : {e}")
        return None, {}

# 1. AUTHENTIFICATION : Login Token
print("[*] Connexion au compte Fandom de LinkRob...")
url_token = "/api.php?action=query&meta=tokens&type=login&format=json"
res, session_cookies = envoyer_requete_fandom(url_token)

if not res or "query" not in res:
    print("[-] Impossible d'initier la connexion. Arrêt.")
    exit(1)

login_token = res["query"]["tokens"]["logintoken"]

# 2. VALIDATION DU LOGIN
donnees_login = {
    "action": "login",
    "lgname": username,
    "lgpassword": password,
    "lgtoken": login_token,
    "format": "json"
}
res_login, cookies_connexion = envoyer_requete_fandom("/api.php", donnees_post=donnees_login, cookies=session_cookies)
session_cookies.update(cookies_connexion)

# Gestion de la double authentification ou de la connexion MediaWiki standard
if not res_login or ("login" in res_login and res_login["login"].get("result") != "Success"):
    print("[-] Échec de l'authentification.")
    if res_login:
        print(f"    Détail du serveur : {res_login.get('login', {}).get('reason', 'Inconnu')}")
    exit(1)

print("[+] Connexion validée ! Session administrateur active.")

# 3. RÉCUPÉRATION DU JETON CSRF (Token d'édition obligatoire)
url_csrf = "/api.php?action=query&meta=tokens&format=json"
res_csrf, _ = envoyer_requete_fandom(url_csrf, cookies=session_cookies)
csrf_token = res_csrf["query"]["tokens"]["csrftoken"]

# 4. PARCOURS ET INJECTION DE MASSE
dossier_source = "siphonnage_de_Fandom"

if not os.path.exists(dossier_source):
    print(f"[-] Erreur : Le dossier /{dossier_source} est introuvable.")
    exit(1)

print("[*] Initialisation du téléversement de masse...")
compteur_succes = 0

for racine, dossiers, fichiers in os.walk(dossier_source):
    for fichier in fichiers:
        if fichier.endswith(".txt"):
            chemin_complet = os.path.join(racine, fichier)
            titre_page = fichier.replace(".txt", "").replace("_", " ")
            
            if "Main Page" in titre_page or "LinkRob Wiki" in titre_page:
                continue
                
            print(f" -> Injection sur le wiki : '{titre_page}'...")
            
            try:
                with open(chemin_complet, "r", encoding="utf-8") as f:
                    contenu_article = f.read()
                
                donnees_edit = {
                    "action": "edit",
                    "title": titre_page,
                    "text": contenu_article,
                    "summary": "Provisionnement automatique par Script DevOps Python",
                    "token": csrf_token,
                    "format": "json"
                }
                
                res_edit, _ = envoyer_requete_fandom("/api.php", donnees_post=donnees_edit, cookies=session_cookies)
                
                if res_edit and "edit" in res_edit and res_edit["edit"].get("result") == "Success":
                    compteur_succes += 1
                    print(f"    [+] Page #{compteur_succes} injectée avec succès.")
                else:
                    print(f"    [-] Modification refusée ou ignorée.")
            except Exception as e:
                print(f"    [-] Erreur : {e}")
                
            time.sleep(1.5)

print(f"\n[++] MISSION ACCOMPLIE ! {compteur_succes} articles ont été clonés sur ton wiki.")
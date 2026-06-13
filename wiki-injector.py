import urllib.request
import urllib.parse
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

print("=== INJECTEUR DEV-OPS MULTITHREADÉ + DISCORD ===")

hote = "://fandom.com"
cookie_session = "MTc4MTM2MDA1NnxjTmJqNTdrck9ncUdzQmM4OXlCV0RPWVNfZGRVZzlZdmVOUlVCbnh4TjRVQlJkUnYzS1FUekZkNmlSVHhqQnAyOW00WGRvX050cUlMQTBhSS02aW9YclVCTUhVRmtpS19XNHpidFRFSXMySlZreDV6c0syQ1ppajdoRUdEY0xMWi0zaTdNN3Qta0MwS2VUWFd4U0dWUC1YQzJJSTlDTFBrLXZMWmNnNlhqX1FDalRRT2RaQzNqQjRKa3hWcUdpWldjcmsycTZoM2FBZ0h0MUp1MlNNZ1Z2ZVQyTzE3YlZYeDhmbVNRLUllS0lRZ0UyLVYyMFQ3Tm1JMWxYSUNKT2xtQi1ZTElTalhSNFdyV3paNEhXQlp8ucZGTR76k6TzKwodNANSmCzJsP_bVj0w-4j8wkDLfks="
URL_WEBHOOK_DISCORD = "https://discord.com"

def notifier_discord(message):
    donnees = json.dumps({"content": message}).encode('utf-8')
    req = urllib.request.Request(URL_WEBHOOK_DISCORD, data=donnees, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r: pass
    except: pass

def envoyer_requete_fandom(chemin_api, donnees_post=None):
    url = f"https://{hote}{chemin_api}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"fandom_session={cookie_session}"
    }
    donnees_encodees = urllib.parse.urlencode(donnees_post).encode('utf-8') if donnees_post else None
    try:
        req = urllib.request.Request(url, data=donnees_encodees, headers=headers, method="POST" if donnees_post else "GET")
        with urllib.request.urlopen(req, timeout=12) as r: 
            return json.loads(r.read().decode('utf-8'))
    except: 
        return None

# 1. INITIALISATION ET JETON CSRF
print("[*] Connexion à l'API centrale...")
res_csrf = envoyer_requete_fandom("/api.php?action=query&meta=tokens&format=json")
if not res_csrf or "query" not in res_csrf:
    print("[-] Session expirée ou cookie révoqué. Reprends ton cookie dans le navigateur !"); exit(1)

csrf_token = res_csrf["query"]["tokens"]["csrftoken"]
print("[+] Authentification validée.")
notifier_discord("🚀 **[DEVOPS BOMBARDEMENT]** Lancement du téléversement en parallèle (Multithreadé) !")

# 2. PRÉPARATION DE LA LISTE DES FICHIERS
dossier_source = "siphonnage_de_Fandom"
taches = []

for racine, _, fichiers in os.walk(dossier_source):
    for fichier in fichiers:
        if fichier.endswith(".txt"):
            titre_page = fichier.replace(".txt", "").replace("_", " ")
            if "Main Page" in titre_page or "LinkRob Wiki" in titre_page:
                continue
            taches.append((os.path.join(racine, fichier), titre_page))

# 3. FONCTION EXÉCUTÉE PAR CHAQUE CANAL SIMULTANÉ
def injecter_fichier(args):
    chemin, titre = args
    try:
        with open(chemin, "r", encoding="utf-8") as f: txt = f.read()
        donnees_edit = {"action": "edit", "title": titre, "text": txt, "summary": "DevOps parallel push", "token": csrf_token, "format": "json"}
        res = envoyer_requete_fandom("/api.php", donnees_post=donnees_edit)
        if res and "edit" in res and res["edit"].get("result") == "Success":
            print(f"[+] Injecté : {titre}")
            notifier_discord(f"📥 **[PARALLÈLE]** Article téléversé : `{titre}`")
        else:
            print(f"[-] Rejeté ou bridé : {titre}")
    except: pass
    time.sleep(0.5) # Respiration minimale par canal

# 4. ACTION : Lancement de 10 connexions en même temps !
print(f"[*] Envoi de {len(taches)} articles via 10 canaux parallèles...")
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(injecter_fichier, taches)

notifier_discord(f"✅ **[MISSION INJECTEUR ACCOMPLIE]** Siphonnage parallèle terminé avec succès !")
print("[++] Fin du script.")
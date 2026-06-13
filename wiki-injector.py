import urllib.request
import urllib.parse
import json
import time
import os

print("=== INJECTEUR DE MASSE CYBER-OUTILS + ALERTE DISCORD ===")

hote = "://fandom.com"

# Ton cookie de session admin actuel
cookie_session = "MTc4MTM2MDA1NnxjTmJqNTdrck9ncUdzQmM4OXlCV0RPWVNfZGRVZzlZdmVOUlVCbnh4TjRVQlJkUnYzS1FUekZkNmlSVHhqQnAyOW00WGRvX050cUlMQTBhSS02aW9YclVCTUhVRmtpS19XNHpidFRFSXMySlZreDV6c0syQ1ppajdoRUdEY0xMWi0zaTdNN3Qta0MwS2VUWFd4U0dWUC1YQzJJSTlDTFBrLXZMWmNnNlhqX1FDalRRT2RaQzNqQjRKa3hWcUdpWldjcmsycTZoM2FBZ0h0MUp1MlNNZ1Z2ZVQyTzE3YlZYeDhmbVNRLUllS0lRZ0UyLVYyMFQ3Tm1JMWxYSUNKT2xtQi1ZTElTalhSNFdyV3paNEhXQlp8ucZGTR76k6TzKwodNANSmCzJsP_bVj0w"

# L'URL de ton Webhook Discord pour le bombardement du salon
URL_WEBHOOK_DISCORD = "https://discord.com"

def notifier_discord(message):
    """Envoie un message flash instantané dans le salon Discord via Webhook"""
    donnees = json.dumps({"content": message}).encode('utf-8')
    req = urllib.request.Request(
        URL_WEBHOOK_DISCORD, 
        data=donnees, 
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 DevOps"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            pass
    except Exception as e:
        print(f"[-] Échec de notification Discord : {e}")

def envoyer_requete_fandom(chemin_api, donnees_post=None):
    """Gère l'envoi de requêtes sécurisées à Fandom en injectant le cookie"""
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

# 1. INITIALISATION ET RÉCUPÉRATION DU JETON CSRF
print("[*] Vérification de la session Fandom...")
url_csrf = "/api.php?action=query&meta=tokens&format=json"
res_csrf = envoyer_requete_fandom(url_csrf)

if not res_csrf or "query" not in res_csrf or "csrftoken" not in res_csrf["query"]["tokens"]:
    print("[-] Session expirée ou cookie fandom_session invalide.")
    exit(1)

csrf_token = res_csrf["query"]["tokens"]["csrftoken"]
print("[+] Connexion établie avec succès.")

# Alerte Discord de lancement
notifier_discord("🚀 **[DEVOPS]** Lancement du script d'injection massive sur LinkRob Wiki !")

# 2. PARCOURS ET INJECTION AUTOMATIQUE SÉQUENTIELLE
dossier_source = "siphonnage_de_Fandom"
if not os.path.exists(dossier_source):
    print(f"[-] Dossier {dossier_source} introuvable.")
    exit(1)

compteur = 0
for racine, _, fichiers in os.walk(dossier_source):
    for fichier in fichiers:
        if fichier.endswith(".txt"):
            chemin_complet = os.path.join(racine, fichier)
            titre_page = fichier.replace(".txt", "").replace("_", " ")
            
            if "Main Page" in titre_page or "LinkRob Wiki" in titre_page:
                continue
                
            try:
                with open(chemin_complet, "r", encoding="utf-8") as f:
                    txt = f.read()
                
                donnees_edit = {
                    "action": "edit",
                    "title": titre_page,
                    "text": txt,
                    "summary": "Provisionnement DevOps automatique via Script Python",
                    "token": csrf_token,
                    "format": "json"
                }
                
                res_edit = envoyer_requete_fandom("/api.php", donnees_post=donnees_edit)
                
                if res_edit and "edit" in res_edit and res_edit["edit"].get("result") == "Success":
                    compteur += 1
                    print(f"[+] Article #{compteur} injecté : {titre_page}")
                    notifier_discord(f"📥 **[Page #{compteur}]** Nouvel article injecté : `{titre_page}`")
                else:
                    print(f"[-] Modification rejetée pour : {titre_page}")
            except Exception as e:
                print(f"[-] Erreur fichier : {e}")
                
            time.sleep(1.3)

notifier_discord(f"✅ **[MISSION TERMINÉE]** Injection finale achevée. `{compteur}` articles synchronisés !")
print(f"\n[++] Succès total. {compteur} fichiers traités.")
import urllib.request
import urllib.parse
import json
import time
import os
import subprocess

print("=== DEVOPS INFINITE SCRAPER & SELF-COMMIT (EXPLOSION MODE) ===")

themes_industriels = [
    "zelda", "mario", "minecraft", "starwars", "pokemon", "naruto", "onepiece", 
    "gta", "fortnite", "witcher", "skyrim", "fallout", "halo", "assassinscreed", 
    "marvel", "dc", "disney", "harrypotter", "lordoftherings", "gameofthrones"
]

def net(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r: 
            return json.loads(r.read().decode("utf-8"))
    except: 
        return None

def executer_git():
    """Force une sauvegarde automatique sur GitHub pour simuler une activité continue"""
    print("\n[➔ KEEP-ALIVE] Envoi des données en cours vers GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Sauvegarde automatique - Moissonnage en cours"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[+] GitHub mis à jour avec succès. Codespace maintenu éveillé.\n")
    except Exception as e:
        print(f"[-] Échec de la sauvegarde Git automatique : {e}\n")

compteur_wikis = 0
dernier_commit_temps = time.time()

for t in themes_industriels:
    hote = f"{t}.fandom.com"
    compteur_wikis += 1
    folder = hote.split(".")[0]
    
    print(f"\n" + "X"*60)
    print(f"[WIKI GLOBAL #{compteur_wikis}] Siphonnage TOTAL de : {hote}")
    print("X"*60)
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    jeton_page = ""
    compteur_articles_wiki = 0
    
    while True:
        # --- LOGIQUE KEEP-ALIVE ---
        # Si plus de 15 minutes (900 secondes) se sont écoulées, on fait un push de sécurité
        if time.time() - dernier_commit_temps > 900:
            executer_git()
            dernier_commit_temps = time.time()

        url_liste = f"https://{hote}/api.php?action=query&list=allpages&aplimit=500&format=json"
        if jeton_page:
            url_liste += f"&apcontinue={urllib.parse.quote(jeton_page)}"
            
        data_pages = net(url_liste)
        if not data_pages or "query" not in data_pages or "allpages" not in data_pages["query"]:
            break
            
        articles = data_pages["query"]["allpages"]
        if not articles:
            break
            
        for p in articles:
            titre = p["title"]
            compteur_articles_wiki += 1
            
            if compteur_articles_wiki % 100 == 0:
                print(f"     -> Progression : {compteur_articles_wiki} articles extraits...")
                
            titre_enc = urllib.parse.quote(titre)
            url_a = f"https://{hote}/api.php?action=query&titles={titre_enc}&prop=revisions&rvprop=content&format=json"
            data_a = net(url_a)
            
            if data_a and "query" in data_a and "pages" in data_a["query"]:
                try:
                    p_id = list(data_a["query"]["pages"].keys())[0]
                    if "revisions" in data_a["query"]["pages"][p_id]:
                        txt = data_a["query"]["pages"][p_id]["revisions"][0]["*"]
                        nom_propre = "".join([c if c.isalnum() or c in "._-" else "_" for c in titre.replace(" ", "_")])
                        nom_f = f"{folder}/{nom_propre[:100]}.txt"
                        
                        with open(nom_f, "w", encoding="utf-8") as f:
                            f.write(txt)
                except:
                    pass
            time.sleep(0.02) # Vitesse maximale
            
        if "continue" in data_pages and "apcontinue" in data_pages["continue"]:
            jeton_page = data_pages["continue"]["apcontinue"]
        else:
            print(f"[+] {hote} entièrement vidé !")
            break

# Push final à la toute fin du script
executer_git()
print("\n[++] TOUS LES MATELOTS SONT AU PORT. GITHUB A SOUFFERT.")
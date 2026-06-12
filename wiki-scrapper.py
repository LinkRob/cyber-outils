import urllib.request
import urllib.parse
import json
import time
import os

print("=== DEVOPS MASTER PROGRESSIVE SCRAPER ===")

# L'arsenal complet des thèmes Fandom à siphonner de manière séquentielle
themes_industriels = [
    "zelda", "mario", "minecraft", "starwars", "pokemon", "naruto", "onepiece", 
    "gta", "fortnite", "witcher", "skyrim", "fallout", "halo", "assassinscreed", 
    "marvel", "dc", "disney", "harrypotter", "lordoftherings", "gameofthrones",
    "dragonball", "bleach", "myheroacademia", "demonslayer", "attackontitan",
    "callofduty", "leagueoflegends", "worldofwarcraft", "eldenring", "darksouls"
]

def net(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=7) as r: 
            return json.loads(r.read().decode("utf-8"))
    except: 
        return None

compteur = 0
for t in themes_industriels:
    # On génère la liste des cibles standards et francophones pour chaque thème
    cibles = [f"{t}.fandom.com", f"{t}-fr.fandom.com"]
    
    for hote in cibles:
        compteur += 1
        folder = hote.split(".")[0]
        
        print(f"\n" + "="*50)
        print(f"[CRAWL #{compteur}] Tentative sur l'hôte : {hote}")
        print("="*50)
        
        # Test de l'API pour voir si le wiki existe
        url_p = f"https://{hote}/api.php?action=query&list=allpages&aplimit=20&format=json"
        data_p = net(url_p)
        
        if not data_p or "query" not in data_p or "allpages" not in data_p["query"]:
            print(f"  [-] Serveur inactif ou inexistant. Passage au suivant.")
            continue
            
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"  [+] Dossier distinct créé : /{folder}")
            
        articles = data_p["query"]["allpages"]
        print(f"  [+] {len(articles)} pages détectées. Extraction séquentielle...")
        
        for p in articles:
            titre = p["title"]
            print(f"     -> Téléchargement de : {titre}")
            
            titre_enc = urllib.parse.quote(titre)
            url_a = f"https://{hote}/api.php?action=query&titles={titre_enc}&prop=revisions&rvprop=content&format=json"
            data_a = net(url_a)
            
            if data_a and "query" in data_a and "pages" in data_a["query"]:
                try:
                    p_id = list(data_a["query"]["pages"].keys())[0]
                    if "revisions" in data_a["query"]["pages"][p_id]:
                        txt = data_a["query"]["pages"][p_id]["revisions"][0]["*"]
                        
                        nom_f = f"{folder}/{titre.replace(' ', '_').replace('/', '_')}.txt"
                        with open(nom_f, "w", encoding="utf-8") as f:
                            f.write(f"WIKI : {hote}\nTITLE : {titre}\n\n" + txt)
                except:
                    pass
            time.sleep(0.2) # Respiration par fichier pour tromper le pare-feu
        time.sleep(1.0) # Respiration entre les serveurs

print("\n[++] TOUTES LES ARCHIVES CONFIGURÉES ONT ÉTÉ EXTRAITES.")
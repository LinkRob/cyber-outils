import urllib.request
import urllib.parse
import json
import time
import os

print("=== DEVOPS INFINITE DURATION MINER ===")

# --- BASE DE DONNÉES DE MASS-MINING ---
# Le script va parcourir cette liste et s'auto-alimenter de façon séquentielle
prefixes_communautaires = [
    "zelda", "mario", "minecraft", "starwars", "pokemon", 
    "naruto", "onepiece", "gta", "fortnite", "witcher",
    "skyrim", "fallout", "halo", "assassinscreed", "marvel"
]

def net(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r: 
            return json.loads(r.read().decode("utf-8"))
    except: 
        return None

compteur_wikis = 0

# BOUCLE PRINCIPALE : Exploration de tout l'écosystème Fandom
for prefixe in prefixes_communautaires:
    # Pour chaque thème, on teste la version standard et les variantes linguistiques
    variantes_domaines = [f"{prefixe}.fandom.com", f"{prefixe}://fandom.com"]
    
    for w in variantes_domaines:
        compteur_wikis += 1
        folder = w.split(".")[0]
        
        print(f"\n" + "="*50)
        print(f"[WIKI #{compteur_wikis}] Analyse de l'hôte : {w}")
        print("="*50)
        
        # Étape 1 : Vérification si le wiki existe en testant son API
        url_p = f"https://{w}/api.php?action=query&list=allpages&aplimit=20&format=json"
        data_p = net(url_p)
        
        if not data_p or "query" not in data_p:
            print(f"  [-] Hôte inactif ou protégé. Passage au suivant.")
            continue
            
        # Étape 2 : Si le wiki répond, on crée son dossier distinct
        if not os.path.exists(folder): 
            os.makedirs(folder)
            print(f"  [+] Répertoire créé : /{folder}")
            
        # Étape 3 : Aspiration séquentielle des articles de ce wiki
        articles = data_p["query"]["allpages"]
        print(f"  [+] {len(articles)} articles détectés. Extraction en cours...")
        
        for p in articles:
            t = p["title"]
            print(f"     -> Extraction de : {t}")
            
            url_a = f"https://{w}/api.php?action=query&titles={urllib.parse.quote(t)}&prop=revisions&rvprop=content&format=json"
            data_a = net(url_a)
            
            if data_a and "query" in data_a and "pages" in data_a["query"]:
                try:
                    p_id = list(data_a["query"]["pages"].keys())[0]
                    if "revisions" in data_a["query"]["pages"][p_id]:
                        txt = data_a["query"]["pages"][p_id]["revisions"][0]["*"]
                        
                        # Rangement propre
                        nom_f = f"{folder}/{t.replace(' ', '_').replace('/', '_')}.txt"
                        with open(nom_f, "w", encoding="utf-8") as f: 
                            f.write(f"SOURCE : {w}\nARTICLE : {t}\n" + "="*30 + "\n\n" + txt)
                except: 
                    pass
            
            # Pause de 0.2 seconde entre chaque fichier pour ne pas surcharger le Chromebook
            time.sleep(0.2)
            
        # Pause de 1 seconde entre chaque wiki pour réinitialiser la connexion SSL
        time.sleep(1.0)

print("\n[++] TOUS LES DOSSIERS ONT ÉTÉ TRAITÉS ET ENREGISTRÉS SANS SATURATION.")
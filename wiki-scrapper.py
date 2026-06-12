import urllib.request
import urllib.parse
import json
import time
import os

print("=== DEVOPS PROGRESSIVE MULTI-WIKI MINER ===")

# --- TA BASE DE CIBLES EN DUR ---
# Tu peux enrichir cette liste avec autant de wikis Fandom valides que tu veux !
wikis_cibles = [
    "zeldawikidelinkrob.fandom.com",
    "zelda.fandom.com",
    "minecraft.fandom.com",
    "starwars.fandom.com",
    "mario.fandom.com"
]

# Tri alphabétique strict de la liste
wikis_alphabetiques = sorted(wikis_cibles)
print(f"[+] {len(wikis_alphabetiques)} wikis chargés dans l'ordre alphabétique.")

def net(u):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r: 
            return json.loads(r.read().decode("utf-8"))
    except: 
        return None

# Boucle séquentielle (1 par 1)
compteur = 0
for w in wikis_alphabetiques:
    compteur += 1
    # On isole le sous-domaine pour faire un nom de dossier propre (ex: minecraft)
    folder = w.split(".")[0]
    print(f"\n[WIKI #{compteur}] Traitement progressif de : {w}")
    
    # Création du dossier distinct si nécessaire
    if not os.path.exists(folder): 
        os.makedirs(folder)
        print(f"   [+] Répertoire créé : /{folder}")
    
    # Récupération des 5 premiers articles du wiki en cours
    url_p = f"https://{w}/api.php?action=query&list=allpages&aplimit=5&format=json"
    data_p = net(url_p)
    
    if data_p and "query" in data_p and "allpages" in data_p["query"]:
        for p in data_p["query"]["allpages"]:
            t = p["title"]
            print(f"   -> Extraction locale de : {t}")
            
            # Récupération du texte brut
            url_a = f"https://{w}/api.php?action=query&titles={urllib.parse.quote(t)}&prop=revisions&rvprop=content&format=json"
            data_a = net(url_a)
            
            if data_a and "query" in data_a and "pages" in data_a["query"]:
                try:
                    p_id = list(data_a["query"]["pages"].keys())[0]
                    if "revisions" in data_a["query"]["pages"][p_id]:
                        txt = data_a["query"]["pages"][p_id]["revisions"][0]["*"]
                        
                        # Écriture propre dans son dossier dédié
                        nom_f = f"{folder}/{t.replace(' ', '_').replace('/', '_')}.txt"
                        with open(nom_f, "w", encoding="utf-8") as f: 
                            f.write(f"SOURCE : {w}\nARTICLE : {t}\n" + "="*30 + "\n\n" + txt)
                except: 
                    pass
            time.sleep(0.2) # Temporisation réseau pour la stabilité du Chromebook
            
print("\n[++] BRAVO PROSPÈRE ! TOUS LES DOSSIERS DISTINCTS SONT ARCHIVÉS.")
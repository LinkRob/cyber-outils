import hashlib
import time

# --- 1. LE SERVEUR (Simulation) ---
# Le mot de passe choisi pour le test est "secret"
MOT_DE_PASSE = "secret"

# On calcule son hash SHA-256 (l'empreinte cryptographique stockée en base de données)
HASH_CIBLE = hashlib.sha256(MOT_DE_PASSE.encode()).hexdigest()

print("=" * 50)
print(f"[SERVEUR] Mot de passe défini : {MOT_DE_PASSE}")
print(f"[SERVEUR] Hash stocké : {HASH_CIBLE}")
print("=" * 50)


# --- 2. LE CRACKER (Attaque par dictionnaire) ---
# Liste de mots de passe courants à tester
dictionnaire = ["123456", "admin", "azerty", "password", "secret", "bienvenue"]

print("\n[*] Lancement de l'attaque par dictionnaire...")
temps_debut = time.time()

succes = False
for tentative in dictionnaire:
    # Pour chaque mot du dictionnaire, on génère son hash SHA-256
    hash_tentative = hashlib.sha256(tentative.encode()).hexdigest()
    
    print(f" -> Test de '{tentative}' : {hash_tentative}")
    
    # On compare avec le hash qu'on cherche à casser
    if hash_tentative == HASH_CIBLE:
        temps_fin = time.time()
        duree = round(temps_fin - temps_debut, 4)
        
        print("\n" + "=" * 50)
        print(f"[SUCCESS] Mot de passe trouvé : '{tentative}'")
        print(f"[*] Trouvé en : {duree} secondes")
        print("=" * 50)
        succes = True
        break

if not succes:
    print("\n[-] Échec : Le mot de passe n'est pas présent dans le dictionnaire.")

import socket

print("=== DEVOPS & CYBER SCANNER INTERACTIF ===")

# Choix de la cible par l'utilisateur
cible = input("Entrez la cible (ex: scanme.nmap.org, ://vulnweb.com, localhost) : ")

if not cible:
    print("[-] Erreur : Vous devez entrer une cible valide.")
    exit(1)

print(f"[*] Analyse de la cible : {cible}")

# Étape 1 : Résolution DNS (Trouver l'IP)
try:
    ip = socket.gethostbyname(cible)
    print(f"[+] Adresse IP de la cible trouvée : {ip}")
except socket.gaierror:
    print("[-] Impossible de résoudre le nom de domaine.")
    exit(1)

# Étape 2 : Sélection du profil de scan
print("\n--- Profils de ports disponibles ---")
print("1. Ports Réseau Standards (22, 80, 443)")
print("2. Ports Applications Web / Dev (8000, 8080, 8443, 8888)")
choix = input("Choisissez un profil (1 ou 2) : ")

if choix == "1":
    ports_cibles = [22, 80, 443]
elif choix == "2":
    ports_cibles = [8000, 8080, 8443, 8888]
else:
    print("[*] Choix invalide. Scan par défaut sur les ports standards.")
    ports_cibles = [22, 80, 443]

# Étape 3 : Scan des ports
print(f"\n[*] Début du scan de ports sur {ip}...")

for port in ports_cibles:
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1.5)
    
    code_port = scanner.connect_ex((ip, port))
    
    if code_port == 0:
        print(f"[+] Port {port} : OUVERT !")
    else:
        print(f"[-] Port {port} : FERMÉ.")
        
    scanner.close()

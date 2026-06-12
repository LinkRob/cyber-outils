import socket

# Configuration de la cible
cible = "scanme.nmap.org"
print(f"[*] Analyse de la cible : {cible}")

# Étape 1 : Résolution DNS (Trouver l'IP)
try:
    ip = socket.gethostbyname(cible)
    print(f"[+] Adresse IP de la cible trouvée : {ip}")
except socket.gaierror:
    print("[-] Impossible de résoudre le nom de domaine.")
    exit(1) # Arrête le script avec un code d'erreur si le DNS échoue

# Étape 2 : Scan des ports stratégiques
ports_cibles = [22, 80, 443, 8080]
print(f"[*] Début du scan de ports sur {ip}...")

for port in ports_cibles:
    # Initialisation du socket réseau pour chaque port
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1.5) # Temps max d'attente en secondes
    
    # Test de connexion
    code_port = scanner.connect_ex((ip, port))
    
    if code_port == 0:
        print(f"[+] Port {port} : OUVERT !")
    else:
        print(f"[-] Port {port} : FERMÉ.")
        
    # Fermeture propre du socket après chaque test
    scanner.close()

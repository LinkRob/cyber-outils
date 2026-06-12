import socket

cible = "scanme.nmap.org"
print(f"[*] Analyse de la cible : {cible}")

try:
    ip = socket.gethostbyname(cible)
    print(f"[+] Adresse IP de la cible trouvée : {ip}")
except socket.gaierror:
    print("[-] Impossible de résoudre le nom de domaine.")
print("[*] Vérification du port 80 (Web)...")
scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scanner.settimeout(2)

code_port = scanner.connect_ex((ip, 80))

if code_port == 0:
    print("[+] Port 80 : OUVERT !")
else:
    print("[-] Port 80 : FERMÉ.")
scanner.close()

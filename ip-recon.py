import socket

cible = "scanme.nmap.org"
print(f"[*] Analyse de la cible : {cible}")

try:
    ip = socket.gethostbyname(cible)
    print(f"[+] Adresse IP de la cible trouvée : {ip}")
except socket.gaierror:
    print("[-] Impossible de résoudre le nom de domaine.")

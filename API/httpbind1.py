import requests

def afficher_json(endpoint):
    url = f"https://httpbin.org/{endpoint}"
    response = requests.get(url)

    # Vérifier que la requête a réussi
    if response.status_code == 200:
        try:
            data = response.json()  # Convertir le JSON en dictionnaire
            print(f"--- Données récupérées depuis /{endpoint} ---")
            print(data)
            print()
        except ValueError:
            print(f"Erreur : la réponse de /{endpoint} n'est pas un JSON valide.")
    else:
        print(f"Erreur HTTP {response.status_code} pour /{endpoint}")

def main():
    endpoints = [
        "get",          # Récupération des données GET
        "ip",           # Voir l'IP client
        "user-agent",   # Voir user-agent
        "headers",      # Voir les headers envoyés
        "uuid",         # Récupérer un UUID
        "status/418"    # Code status personnalisé (418 I'm a teapot)
    ]

    for ep in endpoints:
        afficher_json(ep)

if __name__ == "__main__":
    main()


import requests

def afficher_json(response):
    try:
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print("Données reçues :")
        print(data)
        print("-" * 40)
    except ValueError:
        print("Erreur : la réponse n'est pas un JSON valide.")
        print(response.text)

def test_get():
    print("== GET /get ==")
    response = requests.get("https://httpbin.org/get", params={"param1": "val1", "param2": "val2"})
    afficher_json(response)

def test_post():
    print("== POST /post ==")
    payload = {"username": "chatgpt", "password": "openai"}
    response = requests.post("https://httpbin.org/post", json=payload)
    afficher_json(response)

def test_put():
    print("== PUT /put ==")
    payload = {"update": "true", "id": 123}
    response = requests.put("https://httpbin.org/put", json=payload)
    afficher_json(response)

def test_delete():
    print("== DELETE /delete ==")
    response = requests.delete("https://httpbin.org/delete")
    afficher_json(response)

def main():
    test_get()
    test_post()
    test_put()
    test_delete()

if __name__ == "__main__":
    main()

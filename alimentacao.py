import requests

BASE_URL = "http://localhost:8000/api/"


TOKEN = ""

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

products = [
    
]

def alimentar(endpoint, dados):
    for item in dados:
        response = requests.post(f"{BASE_URL}{endpoint}/", json=item, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Sucesso item {item['name'] if 'name' in item else item}")
        else:
            print(f"Erro ao adicionar item {item['name'] if 'name' in item else item}: {response.status_code} - {response.text}")


alimentar("products", products)
import requests

BASE_URL = "http://localhost:8000/api/"


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyNjQ5ODcyLCJpYXQiOjE3NjI2NDk1NzIsImp0aSI6IjVhNGFhZTlkMTE2YzRmODViMjVmYTY0YjVmNjEzNDgzIiwidXNlcl9pZCI6MX0.OBO_7OISXThlHQ-2QwFoclJFe2hbzsXZNHLtrTEAoFM"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

products = [
    {
        "codigo_product": 2001,
        "name": "Arroz Branco",
        "supplier": 1,  # ID do fornecedor (Fornecedor Alimentos LTDA)
        "category": "NAOPERECIVEIS",
        "barcode": "7891234567890",
        "unit": "KG",
        "quantity": 500
    },
    {
        "codigo_product": 2002,
        "name": "Leite Integral",
        "supplier": 2,  # ID do fornecedor (Distribuidora Bebidas SA)
        "category": "PERECIVEIS",
        "barcode": "7899876543210",
        "unit": "LT",
        "quantity": 200
    },
    {
        "codigo_product": 2003,
        "name": "Caixa de Laranjas",
        "supplier": 1,  # ID do fornecedor (Fornecedor Alimentos LTDA)
        "category": "PERECIVEIS",
        "barcode": "7891112223334",
        "unit": "KG",
        "quantity": 150
    }
]




def alimentar(endpoint, dados):
    for item in dados:
        response = requests.post(f"{BASE_URL}{endpoint}/", json=item, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Sucesso item {item['name'] if 'name' in item else item}")
        else:
            print(f"Erro ao adicionar item {item['name'] if 'name' in item else item}: {response.status_code} - {response.text}")


alimentar("products", products)
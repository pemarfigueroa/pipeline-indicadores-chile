import requests

url = "https://mindicador.cl/api/uf/2026"

resp = requests.get(url)

if resp.status_code == 200:
    dict_uf = resp.json()
    serie_uf = dict_uf["serie"]
    print(f"hay {len(serie_uf)} registros")
    print(serie_uf[0])
    print(serie_uf[1])
else:
    print("Error al conectar con la API:", resp.status_code)

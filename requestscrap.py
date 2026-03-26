import requests
import pandas as pd
import time

BUILD_ID = "KD41YWHMuzlPQhhefsn7D"

HEADERS = {
    "x-nextjs-data": "1",
    "User-Agent": "Mozilla/5.0"
}


def montar_url(path):
    return f"https://apto.vc/_next/data/{BUILD_ID}{path}.json"


def buscar_pagina(path):
    url = montar_url(path)

    res = requests.get(url, headers=HEADERS)

    print("URL:", url)
    print("STATUS:", res.status_code)

    return res.json()


def extrair_cards(data):
    try:
        return data["pageProps"]["realties"]["data"]
    except:
        return []


def parse_card(card):
    return {
        "nome": card.get("name"),
        "endereco": card.get("address"),
        "bairro": card.get("neighborhoods", [{}])[0].get("name"),
        "preco": card.get("price"),
        "area": card.get("area"),
        "quartos": card.get("bedrooms"),
        "banheiros": card.get("bathrooms"),
        "vagas": card.get("parking"),
        "status": card.get("status", {}).get("name"),
        "link": card.get("permalink")
    }


def main():
    path = "/br/rj/rio-de-janeiro"
    todos = []

    while True:
        data = buscar_pagina(path)

        cards = extrair_cards(data)

        if not cards:
            print("🚫 Sem dados")
            break

        print(f"{len(cards)} imóveis")

        for c in cards:
            todos.append(parse_card(c))

        # 👉 pegar próxima página corretamente
        pagination = data["pageProps"]["realties"]

        if not pagination.get("hasMorePages"):
            break

        next_url = pagination.get("nextPageUrl")

        if not next_url:
            break

        path = next_url.replace("?page=", "/page/")

        time.sleep(1)

    df = pd.DataFrame(todos)

    if df.empty:
        print("⚠️ DataFrame vazio")
    else:
        df.to_csv("apartamentos_rio.csv", index=False, sep=";", encoding="utf-8-sig")
        print("✅ CSV salvo!")


if __name__ == "__main__":
    main()
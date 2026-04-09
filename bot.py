def get_items():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    cards = soup.find_all("div")

    for card in cards:
        name = card.find("h3")
        img = card.find("img")

        if name and img:
            text = card.get_text()

            price = "?"
            for word in text.split():
                if word.isdigit():
                    price = word

            items.append({
                "name": name.text.strip(),
                "price": price,
                "image": img["src"]
            })

    return items[:12]

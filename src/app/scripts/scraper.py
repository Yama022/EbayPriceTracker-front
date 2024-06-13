import requests
from bs4 import BeautifulSoup

def fetch_recent_price(search_query):
    search_query_parts = search_query.split()
    url = f"https://www.ebay.fr/sch/i.html?_from=R40&_nkw={'+'.join(search_query_parts)}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    found_recent_sale = False
    recent_sale_price = None
    recent_sale_date = None

    listings = soup.find_all('div', {'class': 's-item__info clearfix'})
    for listing in listings:
        date_element = listing.find('span', {'class': 'POSITIVE'})
        price_element = listing.find('div', {'class': 's-item__detail s-item__detail--primary'}).find('span', {'class': 's-item__price'})
        
        if date_element and price_element:
            recent_sale_date = date_element.text.strip()
            price_text = price_element.text.strip().replace('EUR', '').replace(',', '.').replace(u'\xa0', '').strip()
            try:
                recent_sale_price = float(price_text)
                found_recent_sale = True
                break  # Break after finding the first recent sale
            except ValueError:
                continue

    if not found_recent_sale:
        return None, None  # Retourne None si aucun article récent n'est vendu
    return recent_sale_price, recent_sale_date

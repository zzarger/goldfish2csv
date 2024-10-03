import requests
from bs4 import BeautifulSoup

url = 'https://www.mtggoldfish.com/deck/arena_download/6660345'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

textarea = soup.find('textarea', class_='copy-paste-box')
cards = textarea.get_text().split('\n') if textarea else []
cards = [card for card in cards if card and card.lower() not in ['deck', 'sideboard', 'companion']]

expanded_cards = []
for card in cards:
    count, card_name = card.split(' ', 1)
    expanded_cards.extend([card_name] * int(count))

maindeck = expanded_cards[:-15]
sideboard = expanded_cards[-15:]

result = {'maindeck': maindeck, 'sideboard': sideboard}

print(result)

import requests
from bs4 import BeautifulSoup

def get_deck_cards(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    textarea = soup.find('textarea', class_='copy-paste-box')
    if textarea:
        return textarea.get_text().split('\n')
    return []

def clean_deck_cards(cards):
    # Remove empty items
    cards = [card for card in cards if card and card.lower() not in ['deck', 'sideboard']]
    return cards

def expand_deck_cards(cards):
    expanded_cards = []
    for card in cards:
        print(card)
        parts = card.split(' ', 1)
        count, card_name = parts
        expanded_cards.extend([card_name] * int(count))
    return expanded_cards


    

url = 'https://www.mtggoldfish.com/deck/arena_download/6660345'

cards = get_deck_cards(url)
cards = clean_deck_cards(cards)
cards = expand_deck_cards(cards)

print(cards)




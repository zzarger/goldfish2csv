import csv
import os
import requests

from bs4 import BeautifulSoup

def fetch_deck_data(archetype_url):
    response = requests.get(archetype_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with the class 'btn btn-secondary deck-tools-btn'
    download_links = soup.find_all('a', class_='btn btn-secondary deck-tools-btn')
    for link in download_links:
        if 'Export to Arena' in link.text:
            href = link.get('href')
            download_url = f'https://www.mtggoldfish.com{href}'
            break

    print(download_url)
    response = requests.get(download_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    textarea = soup.find('textarea', class_='copy-paste-box')
    cards = textarea.get_text().split('\n') if textarea else []

    companion_flag = 'companion' in cards[0].lower()
    cards = [card for card in cards if card and card.lower() not in ['deck', 'sideboard', 'companion']]
    if companion_flag:
        cards = cards[1:]

    expanded_cards = []
    for card in cards:
        count, card_name = card.split(' ', 1)
        expanded_cards.extend([card_name] * int(count))

    maindeck = expanded_cards[:-15]
    sideboard = expanded_cards[-15:]

    result = {'maindeck': maindeck, 'sideboard': sideboard}
    return result

front_deck_url = 'https://www.mtggoldfish.com/archetype/legacy-reanimator#paper'
back_deck_url = 'https://www.mtggoldfish.com/archetype/legacy-eldrazi#paper'

front = fetch_deck_data(front_deck_url)
back = fetch_deck_data(back_deck_url)

# Define the CSV file path
csv_file_path = './storage/cards.csv'

# Assert that the front and back decks are the same length
assert len(front['maindeck'] + front['sideboard']) == len(back['maindeck'] + back['sideboard'])

# Prepare the data for CSV
csv_data = []
for front_card, back_card in zip(front['maindeck'] + front['sideboard'], back['maindeck'] + back['sideboard']):
    csv_data.append([1, front_card, '', back_card, ''])

# Create the storage directory if it doesn't exist
os.makedirs('./storage', exist_ok=True)
# Write the data to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Quantity', 'Front', 'Front ID', 'Back', 'Back ID'])
    # Write the card data
    writer.writerows(csv_data)


import json
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

base_path = "C:\\Users\\nezay\\OneDrive\\Bureau\\TP JO"
events = load_json(os.path.join(base_path, 'events.json'))
stadiums = load_json(os.path.join(base_path, 'stadiums.json'))
tickets = load_json(os.path.join(base_path, 'tickets.json'))

font_path = os.path.join(base_path, 'Paris2024.ttf')
font_blue = ImageFont.truetype(font_path, 36)
font_white = ImageFont.truetype(font_path, 22)

ticket_folder = os.path.join(base_path, 'tickets')
os.makedirs(ticket_folder, exist_ok=True)

def format_datetime(iso_str):
    dt = datetime.fromisoformat(iso_str[:-6])
    return dt.strftime("%d/%m/%Y %H:%M")

# Création des billets
for ticket in tickets:
    event = next(e for e in events if e['id'] == ticket['event_id'])
    stadium = next(s for s in stadiums if s['id'] == event['stadium_id'])
    event_start = format_datetime(event['start'])
    
    # Création du QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(ticket['id'])
    qr.make(fit=True)
    img_qr = qr.make_image(fill='black', back_color='white')
    img_qr = img_qr.resize((100, 100))

    # Chargement de l'image de fond du billet
    img = Image.open(os.path.join(base_path, 'ticketJO.png'))
    draw = ImageDraw.Draw(img)
    
    draw.text((37, 426), event['team_home'], font=font_blue, fill=(51, 19, 104))
    draw.text((112, 503), event['team_away'], font=font_blue, fill=(51, 19, 104))
    draw.text((60, 588), f"{stadium['name']}, {stadium['location']}", font=font_white)
    draw.text((60, 656), event_start, font=font_white)
    draw.text((20, 756), ticket['category'], font=font_white)
    draw.text((200, 756), ticket['seat'] if ticket['seat'] != "free" else "Libre", font=font_white)
    draw.text((325, 756), f"{ticket['price']}€" if ticket['currency'] == 'EUR' else f"{ticket['price']}$", font=font_white)
    img.paste(img_qr, (126, 835))

    # Sauvegarde de l'image du billet
    img.save(os.path.join(ticket_folder, f"ticket_{ticket['id']}.png"))

print("Les billets ont été générés avec succès.")

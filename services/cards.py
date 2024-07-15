from flask import jsonify
from services.database import fetch_one

def get_card_details(cursor, card_id):
    query = "SELECT `rank`, `suit` FROM `Cards` WHERE `card_id` = %s"
    card_details = fetch_one(cursor, query, (card_id,))
    return card_details

def validate_card_exists(cursor, card_id):
    card_details = get_card_details(cursor, card_id)
    if not card_details:
        return {"error": "Card details not found"}, 400
    return None

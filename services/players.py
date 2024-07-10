from services.database import fetch_all

def get_all_players(cursor, match_id):
    query = "SELECT `user_id` FROM `Match_Players` WHERE `match_id` = %s ORDER BY `user_id`"
    players = fetch_all(cursor, query, (match_id,))
    return players

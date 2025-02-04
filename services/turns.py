import random
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import execute_query, fetch_all, fetch_one, close_resources

def get_current_turn(match_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()

    query = """
    SELECT `t`.`turn_id`, `t`.`user_id`, `t`.`round_id`, `t`.`rotation_number`
    FROM `Turns` `t`
    INNER JOIN `Rounds` `r` ON `t`.`round_id` = `r`.`round_id`
    WHERE `r`.`match_id` = %s AND `t`.`end_time` IS NULL
    FOR UPDATE;
    """
    return fetch_one(cursor, query, (match_id,))

def validate_user_turn(turn, user_id):
    if not turn:
        return {"error": "No active turn or match does not exist"}, 400
    if turn[1] != user_id:
        return {"error": "Not the authenticated user's turn"}, 403
    return None

def start_turn(cursor, round_id, next_user_id, next_rotation):
    query = """
    INSERT INTO `Turns` (`round_id`, `user_id`, `rotation_number`, `start_time`)
    VALUES (%s, %s, %s, NOW())
    """

    execute_query(cursor, query, (round_id, next_user_id, next_rotation))
    return cursor.lastrowid

def end_turn(cursor, turn_id):
    query = "UPDATE `Turns` SET `end_time` = NOW() WHERE `turn_id` = %s"
    execute_query(cursor, query, (turn_id,))

def get_next_rotation_number(cursor, round_id, next_user_id):
    query = """
    SELECT `rotation_number` FROM `Turns`
    WHERE `round_id` = %s AND `user_id` = %s
    ORDER BY `rotation_number` DESC LIMIT 1
    """
    last_turn = fetch_one(cursor, query, (round_id, next_user_id))
    if last_turn:
        return last_turn[0] + 1
    else:
        return 1

def get_current_turn_details(round_id, user_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(dictionary=True)

    try:
        query = "SELECT `t`.`turn_id` FROM `Turns` `t` WHERE `t`.`round_id` = %s AND `t`.`end_time` IS NULL"
        turn_id = fetch_one(cursor, query, (round_id,))['turn_id']

        if not turn_id:
            return None

        current_turn_details = get_turn_object(turn_id, user_id)

        query = """
        SELECT MAX(`a`.`action_id`) AS `latest_action_id`
        FROM `Actions` `a`
        JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
        WHERE `t`.`round_id` = %s
        """
        latest_action_id = fetch_one(cursor, query, (round_id,))['latest_action_id']  # NULL if no result

        current_turn_details['latest_action_id'] = latest_action_id

        return current_turn_details
    finally:
        close_resources(cursor, connection)

def get_turn_object(turn_id, authenticated_user_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT `t`.`turn_id`, `t`.`user_id`, `t`.`rotation_number`, `t`.`start_time`, `t`.`end_time`,
               `a`.`action_id`, `a`.`action_type`, `a`.`public_details`, `a`.`full_details`
        FROM `Turns` `t`
        LEFT JOIN `Actions` `a` ON `t`.`turn_id` = `a`.`turn_id`
        WHERE `t`.`turn_id` = %s
        ORDER BY `t`.`start_time` DESC, `a`.`action_id` ASC
        """
        result = fetch_all(cursor, query, (turn_id,))

        if result:
            turn_user_id = result[0]['user_id']
            turn_details = {
                "turn_id": result[0]['turn_id'],
                "user_id": turn_user_id,
                "rotation_number": result[0]['rotation_number'],
                "start_time": result[0]['start_time'].strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": result[0]['end_time'].strftime('%Y-%m-%d %H:%M:%S') if result[0]['end_time'] else None,
                "actions": [],
            }

            for row in result:
                if row['action_id']:
                    turn_details["actions"].append({
                        "action_id": row['action_id'],
                        "action_type": row['action_type'],
                        "public_details": row['public_details'],
                        "full_details": row['full_details'] if turn_user_id == authenticated_user_id else None
                    })

            return turn_details
        else:
            return None
    finally:
        close_resources(cursor, connection)

def determine_first_player(match_id, player_ids, cursor):
    previous_round_query = "SELECT `round_id` FROM `Rounds` WHERE `match_id` = %s AND `end_time` IS NOT NULL ORDER BY `start_time` DESC LIMIT 1"
    previous_round = fetch_one(cursor, previous_round_query, (match_id,))

    if previous_round:
        first_player_query = "SELECT `user_id` FROM `Turns` WHERE `round_id` = %s ORDER BY `start_time` ASC LIMIT 1"
        previous_first_player = fetch_one(cursor, first_player_query, (previous_round[0],))[0]
        previous_first_index = player_ids.index(previous_first_player)
        first_player = player_ids[(previous_first_index + 1) % len(player_ids)]
    else:
        first_player = random.choice(player_ids)

    return first_player

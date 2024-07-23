from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import execute_query, fetch_all, fetch_one, close_resources

def get_current_turn(cursor, match_id):
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

def get_current_turn_details(round_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()

    try:
        # Query to find the current turn for the specified round and its actions
        query = """
        SELECT `t`.`turn_id`, `t`.`user_id`, `t`.`rotation_number`, `t`.`start_time`,
               `a`.`action_id`, `a`.`action_type`, `a`.`public_details`
        FROM `Turns` `t`
        LEFT JOIN `Actions` `a` ON `t`.`turn_id` = `a`.`turn_id`
        WHERE `t`.`round_id` = %s AND `t`.`end_time` IS NULL
        ORDER BY `t`.`start_time` DESC, `a`.`action_id` ASC
        """
        result = fetch_all(cursor, query, (round_id,))

        # Query to find the latest action_id associated with the round
        query = """
        SELECT MAX(`a`.`action_id`)
        FROM `Actions` `a`
        JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
        WHERE `t`.`round_id` = %s
        """
        latest_action_id = fetch_one(cursor, query, (round_id,))[0]  # NULL if no result

        if result:
            # Extract turn details from the first row
            turn_details = {
                "turn_id": result[0][0],
                "user_id": result[0][1],
                "rotation_number": result[0][2],
                "start_time": result[0][3].strftime('%Y-%m-%d %H:%M:%S'),
                "actions": [],
                "latest_action_id": latest_action_id
            }

            # Append action details
            for row in result:
                if row[4]:  # Ensure action_id is not None
                    turn_details["actions"].append({
                        "action_id": row[4],
                        "action_type": row[5],
                        "public_details": row[6]
                    })

            return turn_details
        else:
            return None
    finally:
        close_resources(cursor, connection)

from services.database import execute_query, fetch_one

def get_current_turn(cursor, match_id):
    query = """
    SELECT `t`.`turn_id`, `t`.`user_id`, `t`.`round_id`
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

from datetime import datetime
from services.database import execute_query, fetch_one

def get_opening_balance(cursor, user_id, round_id):
    query = """
    SELECT SUM(`sc`.`score_change`)
    FROM `Score_Changes` `sc`
    JOIN `Actions` `a` ON `sc`.`action_id` = `a`.`action_id`
    JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
    JOIN `Rounds` `r` ON `t`.`round_id` = `r`.`round_id`
    WHERE `sc`.`user_id` = %s
    AND `r`.`match_id` = (
        SELECT `match_id` FROM `Rounds` WHERE `round_id` = %s
    )
    AND `r`.`start_time` < (
        SELECT `start_time` FROM `Rounds` WHERE `round_id` = %s
    )
    """
    result = fetch_one(cursor, query, (user_id, round_id, round_id))
    return int(result[0]) if result[0] is not None else 0

def get_round_points(cursor, user_id, round_id):
    query = """
    SELECT SUM(`sc`.`score_change`)
    FROM `Score_Changes` `sc`
    JOIN `Actions` `a` ON `sc`.`action_id` = `a`.`action_id`
    JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
    WHERE `sc`.`user_id` = %s
    AND `t`.`round_id` = %s
    """
    result = fetch_one(cursor, query, (user_id, round_id))
    return int(result[0]) if result[0] is not None else 0

def record_score_change(cursor, action_id, user_id, score_change):
    query = """
    INSERT INTO `Score_Changes` (`action_id`, `user_id`, `change_time`, `score_change`)
    VALUES (%s, %s, %s, %s)
    """
    current_time = datetime.now()
    execute_query(cursor, query, (action_id, user_id, current_time, score_change))

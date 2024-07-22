from datetime import datetime
from services.database import execute_query

def record_score_change(cursor, action_id, user_id, score_change):
    query = """
    INSERT INTO `Score_Changes` (`action_id`, `user_id`, `change_time`, `score_change`)
    VALUES (%s, %s, %s, %s)
    """
    current_time = datetime.now()
    execute_query(cursor, query, (action_id, user_id, current_time, score_change))

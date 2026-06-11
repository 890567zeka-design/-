import sys
import json
import mysql.connector
from collections import defaultdict

DB_CONFIG = {
    'host': 'localhost',
    'database': 'deadnav',
    'user': 'root',
    'password': 'rootpass',
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_tasks(user_id: int = 1) -> dict:
    """
    Возвращает список наград по месяцам
    
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM user_gamification WHERE id = %s
    """, (user_id,))
    
    gamification = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return {
        "message": "Требуется добавить поле month в user_gamification",
        "current_data": gamification
    }


def get_user_statistics(user_id: int = 1) -> dict:
    """Получает всю статистику пользователя по месяцам"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT month, completed_tasks, moved_deadlines, total_tasks
        FROM user_statistics 
        WHERE user_id = %s 
        ORDER BY month DESC
    """, (user_id,))
    
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"statistics": stats}


if __name__ == "__main__":
    user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    result = get_tasks(user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

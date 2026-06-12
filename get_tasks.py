import json
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'demo_bd',
    'password': '',
    'database': 'demo_bd',
    'charset': 'utf8mb4',
    'port': 3306
}

def get_rewards():
    """
    Возвращает все выданные награды пользователя по месяцам.
    Возвращает словарь в формате:
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT month, award_name 
            FROM awards 
            ORDER BY month DESC
        """)
        rows = cursor.fetchall()
        
        rewards = {}
        for month, award in rows:
            if month not in rewards:
                rewards[month] = []
            if award not in rewards[month]:
                rewards[month].append(award)
        
        conn.close()
        return rewards
    except Exception as e:
        print("Ошибка при получении наград:", e)
        return {}


if __name__ == "__main__":
    result = get_rewards()
    print(json.dumps(result, ensure_ascii=False))

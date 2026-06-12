import json
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'demo_bd',
    'password': '',        
    'database': 'demo_bd',
    'charset': 'utf8mb4'
}


def get_rewards():
    """
    Возвращает все награды пользователя, сгруппированные по месяцам.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Получаем все награды
        cursor.execute("""
            SELECT month, award_name 
            FROM awards 
            ORDER BY month DESC
        """)
        rows = cursor.fetchall()
        
        # Группируем награды по месяцам
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

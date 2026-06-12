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
    conn = None
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
        
        return rewards
    except Exception as e:
        print(json.dumps({"error": f"Ошибка при получении наград: {str(e)}"}, ensure_ascii=False))
        return {}
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    result = get_rewards()
    print(json.dumps(result, ensure_ascii=False))

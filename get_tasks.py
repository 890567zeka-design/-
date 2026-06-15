import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'demo_bd',
    'password': '',
    'database': 'demo_bd',
    'charset': 'utf8mb4'
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def get_rewards():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.month, t.award_name 
            FROM awards a
            JOIN award_types t ON t.id = a.award_type_id
            ORDER BY a.month DESC
        """)
        rows = cursor.fetchall()

        rewards = {}
        for month, award in rows:
            if month not in rewards:
                rewards[month] = []
            if award not in rewards[month]:
                rewards[month].append(award)

        return {"status": "success", "rewards": rewards}

    except Exception as e:
        return {"error": f"Ошибка при получении наград: {str(e)}"}
    finally:
        if conn:
            conn.close()

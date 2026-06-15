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


def calculate_next_month(month_str):
    month, year = map(int, month_str.split('.'))
    month += 1
    if month > 12:
        month = 1
        year += 1
    return f"{month:02d}.{year}"


def define_target(user_id, month):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT current_meeting_deadlines, current_transfer_deadlines 
            FROM statistics WHERE user_id = %s AND month = %s
        """, (user_id, month))
        stats = cursor.fetchone()

        if not stats:
            current_meeting = 65.0
            current_transfer = 25.0
        else:
            current_meeting, current_transfer = stats

        target_meeting = round(20 / (1 + 0.0036 * (current_meeting - 1) ** 1.6), 1)
        target_transfer = round(20 / (1 + 0.0036 * (101 - current_transfer) ** 1.6), 1)

        next_month = calculate_next_month(month)

        cursor.execute("""
            INSERT INTO targets (user_id, month, target_meeting_deadlines, target_transfer_deadlines)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                target_meeting_deadlines = VALUES(target_meeting_deadlines),
                target_transfer_deadlines = VALUES(target_transfer_deadlines)
        """, (user_id, next_month, target_meeting, target_transfer))

        conn.commit()

        return {
            "status": "success",
            "target_month": next_month,
            "target_meeting_deadlines": target_meeting,
            "target_transfer_deadlines": target_transfer
        }

    except Exception as e:
        return {"error": f"Ошибка в define_target: {str(e)}"}
    finally:
        if conn:
            conn.close()
            

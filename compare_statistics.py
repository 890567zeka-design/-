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


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def compare_statistics(old_month, new_month):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получаем цели
        cursor.execute("""
            SELECT target_meeting_deadlines, target_transfer_deadlines 
            FROM targets WHERE month = %s
        """, (old_month,))
        targets = cursor.fetchone()
        if not targets:
            return {"error": "Цели для указанного месяца не найдены"}

        target_meeting, target_transfer = targets

        # Получаем статистику
        cursor.execute("""
            SELECT current_meeting_deadlines, current_transfer_deadlines 
            FROM statistics WHERE month = %s
        """, (new_month,))
        stats = cursor.fetchone()
        if not stats:
            return {"error": "Статистика для указанного месяца не найдена"}

        current_meeting, current_transfer = stats
        awarded = []

        # Хранитель Дедлайнов
        if current_meeting >= target_meeting:
            cursor.execute("""
                INSERT IGNORE INTO awards (month, award_type_id)
                SELECT %s, id FROM award_types WHERE award_name = 'Хранитель Дедлайнов'
            """, (new_month,))
            awarded.append("Хранитель Дедлайнов")

        # Твёрдый срок
        if current_transfer <= target_transfer:
            cursor.execute("""
                INSERT IGNORE INTO awards (month, award_type_id)
                SELECT %s, id FROM award_types WHERE award_name = 'Твёрдый срок'
            """, (new_month,))
            awarded.append("Твёрдый срок")

        conn.commit()
        return {"status": "success", "awarded": awarded}

    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

import json
import sys
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'demo_bd',
    'password': '',
    'database': 'demo_bd',
    'charset': 'utf8mb4',
    'port': 3306
}

def get_connection():
    """Создаёт и возвращает подключение к базе данных"""
    return pymysql.connect(**DB_CONFIG)


def calculate_next_month(month_str):
    """Вычисляет следующий месяц в формате MM.YYYY"""
    month, year = map(int, month_str.split('.'))
    month += 1
    if month > 12:
        month = 1
        year += 1
    return f"{month:02d}.{year}"


def define_target(month):
    """
    Рассчитывает цели на следующий месяц на основе текущей статистики
    и сохраняет их в таблицу targets.
    Возвращает: JSON с целями на следующий месяц
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Получаем текущую статистику
    cursor.execute("""
        SELECT current_meeting_deadlines, current_transfer_deadlines 
        FROM statistics WHERE month = %s
    """, (month,))
    stats = cursor.fetchone()
    
    if not stats:
        current_meeting = 65.0
        current_transfer = 25.0
    else:
        current_meeting, current_transfer = stats
    
    # Формулы
    target_meeting = round(20 / (1 + 0.0036 * (current_meeting - 1) ** 1.6), 1)
    target_transfer = round(20 / (1 + 0.0036 * (101 - current_transfer) ** 1.6), 1)
    
    next_month = calculate_next_month(month)
    
    # Сохраняем или обновляем цели
    cursor.execute("""
        INSERT INTO targets (month, target_meeting_deadlines, target_transfer_deadlines)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            target_meeting_deadlines = VALUES(target_meeting_deadlines),
            target_transfer_deadlines = VALUES(target_transfer_deadlines)
    """, (next_month, target_meeting, target_transfer))
    
    conn.commit()
    conn.close()
    
    return {
        "target_meeting_deadlines": target_meeting,
        "target_transfer_deadlines": target_transfer
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"target_meeting_deadlines": 75.0, "target_transfer_deadlines": 20.0}))
        sys.exit(1)
    
    result = define_target(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))

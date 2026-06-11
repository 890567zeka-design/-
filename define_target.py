import sys
import json
import mysql.connector
from datetime import datetime, timedelta

DB_CONFIG = {
    'host': 'localhost',
    'database': 'deadnav',
    'user': 'root',
    'password': 'rootpass',
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def special_formula(current_value: float) -> float:
    if current_value is None or current_value >= 100:
        return 0
    
    x = max(1, min(100, current_value))
    
    try:
        y = 20 / (1 + 0.0036 * ((x - 1) ** 1.6))
        y = round(y, 1)
        
        if current_value + y > 100:
            y = 100 - current_value
        
        return max(0, y)
    except:
        return 5.0

def calculate_percentages(completed_tasks, moved_deadlines, total_tasks):
    """Рассчитывает проценты из сырых данных"""
    if total_tasks == 0:
        return 0, 0
    
    meeting = (completed_tasks / total_tasks) * 100
    transfer = (moved_deadlines / total_tasks) * 100
    
    return round(meeting, 1), round(transfer, 1)

def define_target(month: str, user_id: int = 1, force: bool = False) -> dict:
    """
    Рассчитывает цели на следующий месяц
    
    Параметры:
        month: месяц для расчёта (формат: YYYY-MM-DD)
        force: принудительный пересчёт
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT completed_tasks, moved_deadlines, total_tasks
        FROM user_statistics 
        WHERE user_id = %s AND month = %s
    """, (user_id, month))
    stats = cursor.fetchone()
    
    if not stats:
        cursor.close()
        conn.close()
        return {"error": f"No data for month {month}"}
    
    current_meeting, current_transfer = calculate_percentages(
        stats['completed_tasks'],
        stats['moved_deadlines'],
        stats['total_tasks']
    )
    
    current_date = datetime.strptime(month, '%Y-%m-%d')
    next_date = current_date.replace(day=1) + timedelta(days=32)
    next_date = next_date.replace(day=1)
    next_month = next_date.strftime('%Y-%m-%d')
    

    improvement_meeting = special_formula(current_meeting)
    improvement_transfer = special_formula(100 - current_transfer)
    
    target_meeting = round(current_meeting + improvement_meeting, 1)
    target_transfer = round(max(0, current_transfer - improvement_transfer), 1)
    
    # Сохраняем цели в user_gamification или создаём новую таблицу
    # Пока просто возвращаем результат
    cursor.close()
    conn.close()
    
    return {
        "target_meeting_deadlines": target_meeting,
        "target_transfer_deadlines": target_transfer,
        "improvement_meeting": improvement_meeting,
        "improvement_transfer": improvement_transfer,
        "current_meeting": current_meeting,
        "current_transfer": current_transfer,
        "next_month": next_month
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python define_target.py <month> [--force]"}))
        print(json.dumps({"example": "python define_target.py 2025-04-01"}))
        sys.exit(1)
    
    month = sys.argv[1]
    force = "--force" in sys.argv
    
    result = define_target(month, force=force)
    print(json.dumps(result, ensure_ascii=False, indent=2))

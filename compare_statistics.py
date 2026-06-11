import sys
import json
import mysql.connector
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'database': 'deadnav',
    'user': 'root',
    'password': 'rootpass', 
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def calculate_percentages(completed_tasks, moved_deadlines, total_tasks):
    """Рассчитывает проценты из сырых данных"""
    if total_tasks == 0:
        return 0, 0
    
    meeting = (completed_tasks / total_tasks) * 100
    transfer = (moved_deadlines / total_tasks) * 100
    
    return round(meeting, 1), round(transfer, 1)

def compare_statistics(old_month: str, new_month: str, user_id: int = 1) -> list:
    """
    Сравнивает статистику за два месяца и выдаёт награды
    
    Параметры:
        old_month: месяц с целями (формат: YYYY-MM-DD)
        new_month: месяц для проверки (формат: YYYY-MM-DD)
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
  
    cursor.execute("""
        SELECT completed_tasks, moved_deadlines, total_tasks
        FROM user_statistics 
        WHERE user_id = %s AND month = %s
    """, (user_id, old_month))
    old_stats = cursor.fetchone()
    
    cursor.execute("""
        SELECT completed_tasks, moved_deadlines, total_tasks
        FROM user_statistics 
        WHERE user_id = %s AND month = %s
    """, (user_id, new_month))
    new_stats = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not old_stats or not new_stats:
        return []
    
    old_meeting, old_transfer = calculate_percentages(
        old_stats['completed_tasks'],
        old_stats['moved_deadlines'],
        old_stats['total_tasks']
    )
    
    new_meeting, new_transfer = calculate_percentages(
        new_stats['completed_tasks'],
        new_stats['moved_deadlines'],
        new_stats['total_tasks']
    )
    
    awarded = []
    
    increase = new_meeting - old_meeting
    decrease = old_transfer - new_transfer
    
    if increase >= 5:
        awarded.append("Хранитель Дедлайнов")
    
    if decrease >= 10:
        awarded.append("Твёрдый срок")
    
    return awarded


def validate_month(month: str) -> bool:
    """Проверяет формат месяца YYYY-MM-DD"""
    try:
        datetime.strptime(month, '%Y-%m-%d')
        return True
    except:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python compare_statistics.py <old_month> <new_month>"}))
        print(json.dumps({"example": "python compare_statistics.py 2025-04-01 2025-05-01"}))
        sys.exit(1)
    
    old_month = sys.argv[1]
    new_month = sys.argv[2]
    
    if not validate_month(old_month) or not validate_month(new_month):
        print(json.dumps({"error": "Invalid month format. Use YYYY-MM-DD"}))
        sys.exit(1)
    
    result = compare_statistics(old_month, new_month)
    print(json.dumps(result, ensure_ascii=False))

import json
import sys
import pymysql
import traceback

# === НАСТРОЙКИ ПОДКЛЮЧЕНИЯ К БАЗЕ ===
DB_CONFIG = {
    'host': 'localhost',
    'user': 'demo_bd',
    'password': '',             # ← Введи сюда свой пароль
    'database': 'demo_bd',
    'charset': 'utf8mb4',
    'port': 3306
}

def get_connection():
    """Создаёт и возвращает подключение к базе данных MySQL"""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print("Ошибка подключения к базе:")
        print(e)
        return None


def compare_statistics(old_month, new_month):
    """
    Сравнивает статистику между двумя месяцами и выдаёт награды.
    Возвращает: список выданных наград
    """
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        # Получаем цели, установленные в предыдущем месяце
        cursor.execute("""
            SELECT target_meeting_deadlines, target_transfer_deadlines 
            FROM targets WHERE month = %s
        """, (old_month,))
        targets = cursor.fetchone()
        
        if not targets:
            print(f"Цели для {old_month} не найдены")
            conn.close()
            return []
        
        target_meeting, target_transfer = targets
        
        # Получаем фактическую статистику за новый месяц
        cursor.execute("""
            SELECT current_meeting_deadlines, current_transfer_deadlines 
            FROM statistics WHERE month = %s
        """, (new_month,))
        stats = cursor.fetchone()
        
        if not stats:
            print(f"⚠️ Статистика для {new_month} не найдена")
            conn.close()
            return []
        
        current_meeting, current_transfer = stats
        awarded = []
        
        # Проверка и выдача наград
        if current_meeting >= target_meeting:
            awarded.append("Хранитель Дедлайнов")
            cursor.execute("INSERT IGNORE INTO awards (month, award_name) VALUES (%s, %s)", 
                          (new_month, "Хранитель Дедлайнов"))
        
        if current_transfer <= target_transfer:
            awarded.append("Твёрдый срок")
            cursor.execute("INSERT IGNORE INTO awards (month, award_name) VALUES (%s, %s)", 
                          (new_month, "Твёрдый срок"))
        
        conn.commit()
        return awarded
        
    except Exception as e:
        print("Ошибка выполнения:")
        print(traceback.format_exc())
        return []
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps([]))
        sys.exit(1)
    
    result = compare_statistics(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False))

import json
import sys
import pymysql
import traceback

#Настройки подключения
DB_CONFIG = {
    'host': 'localhost',        # Адрес сервера 
    'port': 3306,               # Порт MySQL 
    'user': 'demo_bd',          # Логин пользователя базы
    'password': '',             # введи свой пароль
    'database': 'demo_bd',      # Название базы данных
    'charset': 'utf8mb4'        # Кодировка для поддержки русского языка
}


def get_connection():
    """
    Создаёт подключение к базе данных MySQL.
pymysql.connect() принимает все параметры из DB_CONFIG
Устанавливает соединение по TCP (порт 3306)
Выполняет авторизацию (логин + пароль)
Выбирает базу данных 'demo_bd' Возвращает объект соединения (conn)
    """"
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(json.dumps({"error": f"Ошибка подключения к базе: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)

def compare_statistics(old_month, new_month):
    """
    Основная функция скрипта.
    Сравнивает статистику за old_month и new_month и выдаёт награды.
    """
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()   # Курсор — это "указатель" для выполнения SQL-запросов
        
        # 1. Получаем цели, которые были поставлены в предыдущем месяце
        cursor.execute("""
            SELECT target_meeting_deadlines, target_transfer_deadlines 
            FROM targets 
            WHERE month = %s
        """, (old_month,))
        targets = cursor.fetchone()
        
        if not targets:
            print(f" Цели для {old_month} не найдены")
            return []
        
        target_meeting, target_transfer = targets
        
        # 2. Получаем фактическую статистику за новый месяц
        cursor.execute("""
            SELECT current_meeting_deadlines, current_transfer_deadlines 
            FROM statistics 
            WHERE month = %s
        """, (new_month,))
        stats = cursor.fetchone()
        
        if not stats:
            print(f"Статистика для {new_month} не найдена")
            return []
        
        current_meeting, current_transfer = stats
        awarded = []
        
        # 3. Проверяем и выдаём награды
        if current_meeting >= target_meeting:
            awarded.append("Хранитель Дедлайнов")
            cursor.execute("INSERT IGNORE INTO awards (month, award_name) VALUES (%s, %s)", 
                          (new_month, "Хранитель Дедлайнов"))
        
        if current_transfer <= target_transfer:
            awarded.append("Твёрдый срок")
            cursor.execute("INSERT IGNORE INTO awards (month, award_name) VALUES (%s, %s)", 
                          (new_month, "Твёрдый срок"))
        
        conn.commit()        # Сохраняем изменения в базе
        return awarded
        
except Exception as e:
        error_msg = f"Ошибка в compare_statistics: {str(e)}"
        print(json.dumps({"error": error_msg}, ensure_ascii=False))
        return []
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"error": "Неверное количество аргументов."}, ensure_ascii=False))
        sys.exit(1)
    
    result = compare_statistics(sys.argv[1], sys.argv[2])
    print(json.dumps(result, ensure_ascii=False))

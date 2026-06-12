import json
import sys

def compare_statistics(old_month, new_month):
    #  Получить targets из БД по old_month
    targets = {
        "target_meeting_deadlines": 75,
        "target_transfer_deadlines": 20
    }
    
    # Получить статистику из БД по new_month
    stats = {
        "current_meeting_deadlines": 82,
        "current_transfer_deadlines": 12
    }
    
    awarded = []
    
    
    if stats["current_meeting_deadlines"] >= targets["target_meeting_deadlines"]:
        awarded.append("Хранитель Дедлайнов")
    

    if stats["current_transfer_deadlines"] <= targets["target_transfer_deadlines"]:
        awarded.append("Твёрдый срок")
    
    # Сохранить награды в БД
    return awarded


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps([], ensure_ascii=False))
        sys.exit(1)
    
    old_month = sys.argv[1]
    new_month = sys.argv[2]
    result = compare_statistics(old_month, new_month)
    print(json.dumps(result, ensure_ascii=False))

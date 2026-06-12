import json
import sys

def calculate_target_meeting_deadlines(x):
    if x <= 1:
        return 100
    y = 20 / (1 + 0.0036 * (x - 1) ** 1.6)
    return round(min(100, max(0, y)), 1)


def calculate_target_transfer_deadlines(x):
    y = 20 / (1 + 0.0036 * (101 - x) ** 1.6)
    return round(min(100, max(0, y)), 1)


def define_target(month):
    # Получить current_... из БД по month
    current_meeting = 65   # пример текущего значения
    current_transfer = 25  # пример текущего значения
    
    target_meeting = calculate_target_meeting_deadlines(current_meeting)
    target_transfer = calculate_target_transfer_deadlines(current_transfer)
    
    # Сохранить в БД для следующего месяца
    # next_month = calculate_next_month(month)
    
    return {
        "target_meeting_deadlines": target_meeting,
        "target_transfer_deadlines": target_transfer
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        default = {"target_meeting_deadlines": 78.4, "target_transfer_deadlines": 18.7}
        print(json.dumps(default, ensure_ascii=False))
        sys.exit(1)
    
    month = sys.argv[1]
    result = define_target(month)
    print(json.dumps(result, ensure_ascii=False))

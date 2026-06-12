import json

def get_rewards():
    # Получить все награды из БД
    rewards = {
        "06.2025": ["Хранитель Дедлайнов", "Твёрдый срок"],
        "05.2025": ["Хранитель Дедлайнов"]
    }
    return rewards


if __name__ == "__main__":
    result = get_rewards()
    print(json.dumps(result, ensure_ascii=False))

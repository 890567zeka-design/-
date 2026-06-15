from flask import Flask, request, jsonify

from compare_statistics import compare_statistics
from define_target import define_target
from get_rewards import get_rewards

app = Flask(__name__)


@app.route('/gamifications_in_stats/compare_statistics', methods=['GET'])
def compare_statistics_route():
    # Запуск кода в модуле compare_statistics.py
    old_month = request.args.get('old_month')
    new_month = request.args.get('new_month')

    if not old_month or not new_month:
        return jsonify({"error": "Не указаны параметры old_month и/или new_month"}), 400

    result = compare_statistics(old_month, new_month)
    return jsonify(result), 200


@app.route('/gamifications_in_stats/define_target', methods=['GET'])
def define_target_route():
    # Запуск кода в модуле define_target.py
    month = request.args.get('month')

    if not month:
        return jsonify({"error": "Не указан параметр month"}), 400

    result = define_target(month)
    return jsonify(result), 200


@app.route('/gamifications_in_stats/get_rewards', methods=['GET'])
def get_rewards_route():
    # Запуск кода в модуле get_rewards.py
    result = get_rewards()
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=5000)

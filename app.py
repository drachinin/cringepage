from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
import csv
import json
from io import StringIO
import os

app = Flask(__name__)

# Переменные для хранения кликов (для упрощения примера)
clicks_today = 0
clicks_month = 0
total_clicks = 0

# Текущая дата для отслеживания смены дня и месяца
current_day = datetime.now().day
current_month = datetime.now().month

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для обновления счётчика кликов
@app.route('/click', methods=['POST'])
def click():
    global clicks_today, clicks_month, total_clicks, current_day, current_month

    # Проверяем смену дня
    today = datetime.now().day
    if today != current_day:
        clicks_today = 0  # Обнуляем счётчик кликов за день
        current_day = today

    # Проверяем смену месяца
    month = datetime.now().month
    if month != current_month:
        clicks_month = 0  # Обнуляем счётчик кликов за месяц
        current_month = month

    # Увеличиваем счетчики
    clicks_today += 1
    clicks_month += 1
    total_clicks += 1

    # Возвращаем обновлённые данные
    stats = {
        'dailyClicks': clicks_today,
        'monthlyClicks': clicks_month,
        'totalClicks': total_clicks
    }
    return jsonify(stats)

# Маршрут для получения текущей статистики
@app.route('/stats')
def stats():
    global clicks_today, clicks_month, total_clicks, current_day, current_month

    # Проверяем смену дня и месяца для корректного отображения
    today = datetime.now().day
    if today != current_day:
        clicks_today = 0  # Обнуляем счётчик кликов за день
        current_day = today

    month = datetime.now().month
    if month != current_month:
        clicks_month = 0  # Обнуляем счётчик кликов за месяц
        current_month = month

    # Отправляем текущую статистику
    stats = {
        'dailyClicks': clicks_today,
        'monthlyClicks': clicks_month,
        'totalClicks': total_clicks
    }
    return jsonify(stats)

# Маршрут для выгрузки статистики в CSV
@app.route('/export/csv', methods=['GET'])
def export_csv():
    # Создаем CSV файл в памяти (вместо записи на диск)
    output = StringIO()
    writer = csv.writer(output)

    # Пишем заголовки столбцов
    writer.writerow(['Date', 'Clicks Today', 'Clicks This Month', 'Total Clicks'])

    # Пишем строки с данными
    writer.writerow([datetime.now().strftime("%Y-%m-%d"), clicks_today, clicks_month, total_clicks])

    output.seek(0)

    # Отправляем файл на скачивание
    return send_file(output, mimetype='text/csv', as_attachment=True, attachment_filename='statistics.csv')

# Маршрут для выгрузки статистики в JSON
@app.route('/export/json', methods=['GET'])
def export_json():
    # Формируем данные
    data = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'clicks_today': clicks_today,
        'clicks_month': clicks_month,
        'total_clicks': total_clicks
    }

    # Возвращаем JSON-данные
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))



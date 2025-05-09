from flask import Flask, request, jsonify
from flask_cors import CORS  # Импортируем CORS
from datetime import datetime, timedelta

app = Flask(__name__)

# Включаем CORS для всех доменов
CORS(app)

# Тестовая база данных всех рейсов
flights_db = [
    {"from": "Пермь", "to": "Москва", "departure": "2025-05-10 10:00:00", "arrival": "2023-05-10 12:00:00", "probability_on_time": 95},
    {"from": "Пермь", "to": "Москва", "departure": "2025-05-10 13:00:00", "arrival": "2023-05-10 15:00:00", "probability_on_time": 92},
    {"from": "Пермь", "to": "Москва", "departure": "2025-05-10 16:00:00", "arrival": "2023-05-10 18:00:00", "probability_on_time": 80},
    {"from": "Пермь", "to": "Москва", "departure": "2025-05-10 19:00:00", "arrival": "2023-05-10 21:00:00", "probability_on_time": 85},
    {"from": "Москва", "to": "Дубай", "departure": "2025-05-10 13:30:00", "arrival": "2023-05-10 18:00:00", "probability_on_time": 90},
    {"from": "Москва", "to": "Дубай", "departure": "2025-05-10 16:30:00", "arrival": "2023-05-10 21:00:00", "probability_on_time": 88},
    {"from": "Москва", "to": "Дубай", "departure": "2025-05-10 18:00:00", "arrival": "2023-05-10 22:30:00", "probability_on_time": 85},
    {"from": "Москва", "to": "Дубай", "departure": "2025-05-10 20:00:00", "arrival": "2023-05-11 00:30:00", "probability_on_time": 80},
]

# Функция для вычисления вероятности и минимального времени пересадки
def calculate_probability_and_layover(departure_time, arrival_city, departure_city):
    # Преобразуем время в формат datetime
    departure_time = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M")
    
    # Находим все рейсы, которые отправляются из указанного города
    outgoing_flights = [f for f in flights_db if f["from"] == departure_city]

    # Перебираем все рейсы, которые идут из города отправления
    possible_routes = []
    for flight in outgoing_flights:
        # Ищем рейсы из города прибытия
        connecting_flights = [f for f in flights_db if f["from"] == flight["to"] and f["to"] == arrival_city]
        
        for connecting_flight in connecting_flights:
            # Вычисляем время пересадки
            arrival_time = datetime.strptime(flight["arrival"], "%Y-%m-%d %H:%M:%S")
            connecting_departure_time = datetime.strptime(connecting_flight["departure"], "%Y-%m-%d %H:%M:%S")
            layover_time = (connecting_departure_time - arrival_time).total_seconds() / 60  # Переводим в минуты
            
            # Если пересадка возможна, то добавляем в список
            if layover_time >= 60:  # минимум 1 час на пересадку
                possible_routes.append({
                    "first_leg": flight,
                    "second_leg": connecting_flight,
                    "layover_time": layover_time,
                    "probability": (flight["probability_on_time"] + connecting_flight["probability_on_time"]) / 2,
                    "transfer_city": flight["to"]  # Город пересадки
                })
    
    if not possible_routes:
        return {"error": "No valid transfer routes found."}
    
    # Сортируем маршруты по вероятности (от наибольшей к наименьшей)
    best_route = max(possible_routes, key=lambda r: r["probability"])

    # Рассчитываем время вылета из города отправления
    time_to_departure = datetime.strptime(best_route["first_leg"]["arrival"], "%Y-%m-%d %H:%M:%S") - timedelta(minutes=best_route["layover_time"])
    required_departure_time = time_to_departure - timedelta(hours=3)  # Время вылета из города отправления с учетом пересадки

    return {
        "probability": best_route["probability"],
        "layoverTime": best_route["layover_time"],
        "requiredDepartureTime": required_departure_time.strftime("%Y-%m-%d %H:%M:%S"),
        "transferCity": best_route["transfer_city"]  # Добавляем город пересадки
    }

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    departure_time = data.get('departureTime')
    arrival_city = data.get('arrivalCity')
    departure_city = data.get('departureCity')

    if not departure_time or not arrival_city or not departure_city:
        return jsonify({"error": "Missing required fields"}), 400

    result = calculate_probability_and_layover(departure_time, arrival_city, departure_city)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

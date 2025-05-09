import React, { useState } from "react";
import "./App.css"; // Подключаем CSS

function App() {
  const [departureTime, setDepartureTime] = useState("");
  const [arrivalCity, setArrivalCity] = useState("");
  const [departureCity, setDepartureCity] = useState(""); // Новое поле для города отправления
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Формируем тело запроса с городом отправления
    const requestBody = {
      departureTime,
      arrivalCity,
      departureCity, // Добавляем город отправления
    };

    try {
      // Отправка запроса с помощью fetch
      const response = await fetch("http://localhost:5000/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      // Проверка на успешный ответ
      if (!response.ok) {
        throw new Error("Request failed with status " + response.status);
      }

      // Получаем данные из ответа
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error calculating flight:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Flight Planner</h1>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Departure City"
          value={departureCity}
          onChange={(e) => setDepartureCity(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Arrival City"
          value={arrivalCity}
          onChange={(e) => setArrivalCity(e.target.value)}
          required
        />

        <input
          type="datetime-local"
          value={departureTime}
          onChange={(e) => setDepartureTime(e.target.value)}
          required
        />
        
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Check Flight"}
        </button>
      </form>

      {result && (
        <div className="results">
          <h2>Results:</h2>
          {result.error ? (
            <p className="error">{result.error}</p>
          ) : (
            <>
              <p>Вероятность прилететь вовремя: {result.probability}%</p>
              <p>Ожидаемое время пересадки: {result.layoverTime} minutes</p>
              <p>Город пересадки: {result.transferCity}</p>
              <p>Рекомендуемое время вылета из {departureCity}: {result.requiredDepartureTime}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;

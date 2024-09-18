// Обработка нажатия картинки-кнопки
document.getElementById('clickButton').addEventListener('click', function() {
    fetch('/click', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Обновляем статистику после нажатия кнопки
        updateStats(data);
    })
    .catch(error => console.error('Ошибка:', error));
});

// Функция для обновления статистики на странице
function updateStats(data) {
    document.getElementById('dailyClicks').textContent = data.dailyClicks;
    document.getElementById('monthlyClicks').textContent = data.monthlyClicks;
    document.getElementById('totalClicks').textContent = data.totalClicks;
}

// Функция для получения статистики при загрузке страницы
function getStats() {
    fetch('/stats')
    .then(response => response.json())
    .then(data => {
        // Обновляем статистику при загрузке страницы
        updateStats(data);
    })
    .catch(error => console.error('Ошибка при получении статистики:', error));
}

// Получаем статистику при загрузке страницы
window.onload = getStats;

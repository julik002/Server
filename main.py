from flask import Flask, request, jsonify, render_template_string
import re

app = Flask(__name__)

# Временное хранилище для данных пользователей
users = []

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Добро пожаловать!</title>
        <style>
            body {
                background-color: #FFB6C1; /* Нежно-розовый цвет */
                font-family: Arial, sans-serif;
            }
            h1 {
                text-align: center;
            }
            form {
                max-width: 400px;
                margin: auto; /* Центруем форму */
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            label, input, button {
                display: block;
                width: 100%;
                margin-bottom: 10px;
            }
            button {
                background-color: #FF69B4; /* Более яркий розовый для кнопки */
                color: white;
                border: none;
                padding: 10px;
                cursor: pointer;
            }
            button:hover {
                background-color: #FF1493; /* Темно-розовый при наведении */
            }

            /* Стиль для всплывающего окна */
            .modal {
                display: none; /* Скрыто по умолчанию */
                position: fixed; /* Окно фиксируется */
                z-index: 1000; /* Слой над другими элементами */
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5); /* Полупрозрачный фон */
                justify-content: center;
                align-items: center;
            }
            .modal-content {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }
            .close {
                cursor: pointer;
                color: #FF69B4; /* Цвет кнопки закрытия */
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Добро пожаловать!</h1>
        <form id="userForm">
            <label for="name">Имя:</label>
            <input type="text" id="name" name="name" required>
            <label for="email">Электронная почта:</label>
            <input type="email" id="email" name="email">
            <label for="phone">Номер телефона:</label>
            <input type="text" id="phone" name="phone" required>
            <label for="address">Адрес:</label>
            <input type="text" id="address" name="address" required>
            <button type="submit">Отправить</button>
        </form>

        <!-- Всплывающее окно -->
        <div id="modal" class="modal">
            <div class="modal-content">
                <span id="close" class="close">&times;</span>
                <div id="response"></div>
            </div>
        </div>

        <script>
            document.getElementById('userForm').onsubmit = async function(e) {
                e.preventDefault();
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const phone = document.getElementById('phone').value;
                const address = document.getElementById('address').value;

                const response = await fetch('/check', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: name, email: email, phone: phone, address: address })
                });

                const data = await response.json();
                document.getElementById('response').textContent = data.message || data.status;
                document.getElementById('modal').style.display = 'flex'; // Показываем модальное окно
            };

            // Закрытие модального окна
            document.getElementById('close').onclick = function() {
                document.getElementById('modal').style.display = 'none';
            };

            // Закрытие модального окна при клике вне него
            window.onclick = function(event) {
                const modal = document.getElementById('modal');
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            };
        </script>
    </body>
    </html>
    ''')


@app.route('/check', methods=['POST'])
def check_data():
    data = request.json

    # Проверка имени
    if 'name' not in data or not data['name'].strip() or len(data['name'].strip()) < 2:
        return jsonify({"status": "error", "message": "Имя должно содержать не менее 2 символов!"}), 400

    # Проверка электронной почты
    if 'email' in data and data['email'].strip():
        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_pattern, data['email']):
            return jsonify({"status": "error", "message": "Некорректный формат электронной почты!"}), 400

    # Проверка номера телефона
    if 'phone' not in data or not data['phone'].strip():
        return jsonify({"status": "error", "message": "Номер телефона не может быть пустым!"}), 400

    phone_pattern = r"^\d{10}$"  # Шаблон для 10-значного номера
    if not re.match(phone_pattern, data['phone']):
        return jsonify({"status": "error", "message": "Номер телефона должен содержать 10 цифр!"}), 400

    # Проверка адреса
    if 'address' not in data or not data['address'].strip():
        return jsonify({"status": "error", "message": "Адрес не может быть пустым!"}), 400

    # Проверка длины адреса
    if len(data['address'].strip()) < 20:
        return jsonify({"status": "error", "message": "Адрес должен содержать не менее 20 символов!"}), 400

    # Сохранение пользователя в памяти
    users.append({
        "name": data['name'],
        "email": data.get('email'),
        "phone": data['phone'],
        "address": data['address']
    })

    return jsonify({"status": "success", "message": "Данные успешно сохранены!"}), 200


if __name__ == '__main__':
    app.run(debug=True)

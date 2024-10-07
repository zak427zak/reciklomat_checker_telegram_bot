import logging
import os

from flask import Flask, request, jsonify
from werkzeug.http import HTTP_STATUS_CODES

from infrastructure.database.models.base import db
from infrastructure.database.repo.users import UserRepo

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат вывода
                    handlers=[logging.StreamHandler()])  # Вывод логов в консоль

# Настройка базы данных из переменных окружения
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'mysql+pymysql://reciklomat_adm:25HE3V2DXE6defwx3GS66N@reciklomat_mysql:3306/reciklomat')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем базу данных с приложением
db.init_app(app)

# Создание экземпляров репозиториев
user_repo = UserRepo(db.session)


def bad_request(message):
    return error_response(400, message)


def not_found(message):
    return error_response(404, message)


def error_response(status_code, message=None):
    payload = {'errorStatus': HTTP_STATUS_CODES.get(status_code, 'Unknown error'), 'errorCode': "1",
               'errorMessage': str(message), }
    response = jsonify(payload)
    response.status_code = status_code
    return response


@app.route('/user/register', methods=['POST'])
def coffiary_register_new_user():
    payload = request.get_json() or request.form
    # logging.info(f"Received registration payload: {payload}")

    try:
        user = user_repo.get_or_create_user(**payload)
        # logging.info(f"User registered or updated: {user}")
        return 'ok'
    except Exception as e:
        logging.error(f"Error in user registration: {e}")
        return 'error', 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

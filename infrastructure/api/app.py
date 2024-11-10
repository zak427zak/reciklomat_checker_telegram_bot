import logging
import os
from datetime import datetime, timedelta

import requests
from flask import Flask, request, jsonify
from flask_babel import Babel, lazy_gettext as _l
from werkzeug.http import HTTP_STATUS_CODES

from infrastructure.database.models.base import db
from infrastructure.database.repo.reciklomat import ReciklomatRepo
from infrastructure.database.repo.reciklomat_change_history import ReciklomatChangeHistoryRepo
from infrastructure.database.repo.reciklomat_subscription import ReciklomatSubscriptionRepo
from infrastructure.database.repo.users import UserRepo

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG,  # Уровень логирования
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат вывода
                    handlers=[logging.StreamHandler()])  # Вывод логов в консоль

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'mysql+pymysql://reciklomat_adm:25HE3V2DXE6defwx3GS66N@reciklomat_mysql:3306/reciklomat')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)
babel = Babel(app)


# Репозитории
reciklomat_repo = ReciklomatRepo(db.session)
user_repo = UserRepo(db.session)
subscription_repo = ReciklomatSubscriptionRepo(db.session)
history_repo = ReciklomatChangeHistoryRepo(db.session)


def get_locale():
    data = request.get_json() or request.form

    if 'telegram_id' in data:
        user = user_repo.get_by_telegram_id(data['telegram_id'])
        if user and user.language:
            return user.language

    return 'sr'


# @babel.locale_selector_func
# def get_locale():
#     # Получаем telegram_id из запроса
#     data = request.get_json() or request.form
#
#     if 'telegram_id' in data:
#         user = user_repo.get_by_telegram_id(data['telegram_id'])
#         if user and user.language:
#             return user.language  # Возвращаем язык, сохраненный у пользователя
#
#     # Если пользователь не найден, используем язык по умолчанию (например, 'ru')
#     return 'ru'


statuses = {"u prekidu": "На паузе (не работает)", "popunjen": "Заполнен", "u radu": "Работает",
            "artikal zaglavljen": "Что-то застряло (не работает)", "u not working": "Выключен",
            'servisiranje': 'На обслуживании'}

statuses_markers = {"На паузе (не работает)": "🟠", "Заполнен": "🟠", "Что-то застряло (не работает)": "🟠",
                    'На обслуживании': "🟠", "Работает": "🟢", "Выключен": "🔴"}

statuses_markers_translated = {"На паузе (не работает)": _l("На паузе (не работает)"), "Заполнен": _l("Заполнен"),
                               "Что-то застряло (не работает)": _l("Что-то застряло (не работает)"),
                               "На обслуживании": _l("На обслуживании"), "Работает": _l("Работает"),
                               "Выключен": _l("Выключен")}


# Общие функции для обработки ошибок
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


# Маршрут для обновления данных рецикломатов
@app.route('/update-data', methods=['GET'])
def reciklomat_update_data():
    url = 'http://65.21.206.110:8081/RecikliranjeWebApp/GetWebAdditionalData1?_=1704367291000'
    r = requests.get(url)
    data = r.json()

    for item in data['_reciklomati']:
        current_reciklomat = reciklomat_repo.get_by_address(item['_adresa_prodajnog_mesta'])
        if current_reciklomat:
            check_if_status_changes(current_reciklomat, item)
            reciklomat_repo.update_status_by_address(address=item['_adresa_prodajnog_mesta'],
                                                     status=item['_status_prodajnog_mesta'],
                                                     occupancy=int(item['_broj_artikala']),
                                                     capacity=int(item['_max_broj_artikala']),
                                                     last_check=datetime.utcnow() + timedelta(hours=3))
        else:
            new_reciklomat = reciklomat_repo.add_new_reciklomat(address=item['_adresa_prodajnog_mesta'],
                                                                status=item['_status_prodajnog_mesta'],
                                                                occupancy=int(item['_broj_artikala']),
                                                                capacity=int(item['_max_broj_artikala']),
                                                                lat=item['_latitude'], lon=item['_longitude'],
                                                                city=item['_mesto'],
                                                                district=item['_naziv_prodajnog_mesta'])
    return 'ok'


# Проверка изменений статуса и запись в историю
def check_if_status_changes(current_reciklomat, new_reciklomat_data):
    new_status = new_reciklomat_data['_status_prodajnog_mesta']
    if current_reciklomat.status != new_status:
        history_repo.write_status_change(current_reciklomat.id, current_reciklomat.status, new_status)
        if new_status == "Работает":
            send_notifications_to_subscribers(new_reciklomat_data)


# Отправка уведомлений подписчикам
def send_notifications_to_subscribers(new_reciklomat):
    subscribers = subscription_repo.get_by_address(new_reciklomat['_adresa_prodajnog_mesta'])
    for subscriber in subscribers:
        current_subscriber = user_repo.get_by_id(subscriber.user_id)
        if current_subscriber.is_telegram_on:
            send_message_to_telegram(new_reciklomat, current_subscriber)


# Отправка сообщения в Telegram
def send_message_to_telegram(new_reciklomat, subscriber):
    url_tg = 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage'

    message_text = f'<b>{new_reciklomat["_adresa_prodajnog_mesta"]}</b>\n' \
                   f'Заполнено: {new_reciklomat["_broj_artikala"]} из {new_reciklomat["_max_broj_artikala"]}\n' \
                   f'Осталось: {int(new_reciklomat["_max_broj_artikala"]) - int(new_reciklomat["_broj_artikala"])}\n'

    message_data = {'chat_id': subscriber.telegram_id, 'text': message_text, 'parse_mode': 'HTML'}

    requests.post(url_tg, data=message_data)


@app.route('/user/wishlist', methods=['POST'])
def user_wishlist():
    data = request.get_json() or request.form
    current_usr = user_repo.get_by_telegram_id(data['telegram_id'])

    if not current_usr:
        return not_found(_l('Не можем найти вас в системе. Напишите что-нибудь боту, чтобы он авторизовал вас'))

    record_a_visit(current_usr)
    # login_user(current_usr, True)

    # Получаем все рецикломаты и преобразуем их в коллекцию с поддержкой пагинации
    reciklomats_list = reciklomat_repo.to_collection_reciklomats(1, 999, current_usr)

    text_data = _l(
        "Вот список всех рецикломатов:\n\n✅ - уже в вашем вишлисте\n⛔ - нет в вашем вишлисте\n\nНажмите на нужный рецикломат, чтобы добавить или удалить его из вишлиста")

    di = {'items': reciklomats_list, 'text': text_data}

    return jsonify({'result': di})


@app.route('/check', methods=['POST'])
def check():
    payload = request.get_json() or request.form

    # Получаем пользователя через репозиторий
    current_usr = user_repo.get_by_telegram_id(payload['telegram_id'])
    if not current_usr:
        return not_found(_l("Пользователя не существует! Попробуйте ещё раз, или вернитесь позже!"))

    # Обновляем последнее время посещения
    record_a_visit(current_usr)
    # login_user(current_usr, True)

    # Проверяем, есть ли подписки на рецикломаты у пользователя
    if subscription_repo.get_by_user_id(current_usr.id) or payload['howMany'] == "all":
        reciklomats_list = []

        # Получаем все рецикломаты, отсортированные по статусу и занятости
        all_reciklomats = reciklomat_repo.get_all_sorted_by_status_and_occupancy()

        for item in all_reciklomats:
            checker = False

            # Определяем, нужно ли выводить все рецикломаты или только подписанные
            if payload['howMany'] == "all":
                checker = True
            else:
                # Проверяем подписку на данный рецикломат
                if subscription_repo.check_user_subscription(current_usr.id, item.address):
                    checker = True

            # Формируем результат для отображения
            if checker:
                if item.lat == 0 or item.lon == 0:
                    link = f"https://www.google.ru/maps/place/{item.address}"
                else:
                    link = f"https://www.google.ru/maps/place/{item.lat},{item.lon}"

                a1 = _l("Статус рецикломата:")
                a2 = _l("Заполнено:")
                a3 = _l("Осталось места:")
                a4 = _l("из")

                build_result = f"<a href='{link}'>{statuses_markers[item.status]} {item.address}</a>\n" \
                               f"{a1} {statuses_markers_translated[item.status]}\n" \
                               f"{a2} {int(item.occupancy)} {a4} {int(item.capacity)}\n" \
                               f"{a3} {int(item.capacity) - int(item.occupancy)}"

                data_text = {'text': build_result}
                reciklomats_list.append(data_text)

        # Возвращаем список рецикломатов
        return jsonify({'result': reciklomats_list})
    else:
        # Если вишлист пуст
        return not_found(
            _l("Ваш вишлист ещё пуст. Сначала добавите в него рецикломаты - воспользуйтесь командой /wishlist"))


@app.route('/user/register', methods=['POST'])
def reciklomat_register_new_user():
    payload = request.get_json() or request.form

    try:
        user = user_repo.get_or_create_user(**payload)
        logging.info(f"User registered or updated: {user}")
        return jsonify({'result': _l(
            "Привет! Это бот для проверки статусов рецикломатов в Белграде (Сербия).\n\nБот позволяет проверять заполненность всех рецикломатов в реальном времени - команда /all\n\nА ещё можно собрать свой вишлист рецикломатов, которые бот будет отслеживать. Если один из рецикломатов в вашем вишлисте изменит статус на освободился - вы тут же получите уведомление.\n\nДля работы с вишлистом используйте /wishlist\nПроверить статус рецикломатов в вишлисте можно командой /check\n\nДругие доступные команды вы найдете в меню")})

    except Exception as e:
        logging.error(f"Error in user registration: {e}")
        return 'error', 500


@app.route('/user/status', methods=['POST'])
def reciklomat_user_status():
    data = request.get_json() or request.form

    # Проверяем наличие userId в данных
    if 'telegram_id' not in data:
        return bad_request('Поле telegram_id обязательно для заполнения')

    # Получаем пользователя по telegram_id через репозиторий
    current_usr = user_repo.get_by_telegram_id(data['telegram_id'])
    if not current_usr:
        return not_found('Не можем найти вас в системе. Напишите что-нибудь боту, чтобы он авторизовал вас')

    # Обновляем время последнего посещения
    record_a_visit(current_usr)

    # Возвращаем соответствующий ответ в зависимости от статуса подписки
    if current_usr.is_telegram_on:
        return jsonify({'result': _l(
            "Сейчас подписка на статусы ваших рецикломатов включена.\n\nВы будете получать уведомления, как только один из них освободится")})
    else:
        return jsonify({'result': _l(
            "Сейчас подписка на статусы ваших рецикломатов отключена.\n\nВы НЕ будете получать уведомления, как только один из них освободится")})


@app.route('/user/switch/<switch_type>', methods=['POST'])
def user_status_switch(switch_type):
    # Устанавливаем локаль вручную
    babel.locale_selector_func = get_locale

    data = request.get_json() or request.form

    if 'telegram_id' not in data:
        return bad_request('Поле telegram_id обязательно для заполнения')

    current_usr = user_repo.get_by_telegram_id(data['telegram_id'])
    if not current_usr:
        return not_found('Не можем найти вас в системе. Напишите что-нибудь боту, чтобы он авторизовал вас')

    # Обновляем время последнего посещения
    record_a_visit(current_usr)

    # Изменение статуса подписки через метод репозитория
    if switch_type == "off":
        user_repo.update_subscription_status(current_usr.id, False)
        return jsonify(
            {'result': _l("Вы отключили подписку на изменение статусов ваших рецикломатов (которые в вишлисте)")})
    else:
        user_repo.update_subscription_status(current_usr.id, True)
        return jsonify(
            {'result': _l("Вы включили подписку на изменение статусов ваших рецикломатов (которые в вишлисте)")})


@app.route('/help', methods=['POST'])
def help():
    payload = request.get_json() or request.form
    check_user = user_repo.get_by_telegram_id(payload['telegram_id'])
    if check_user:
        return not_found(
            _l("Пожелания, предложения и обратная связь - @German_goncharov\n\nP.S. Бот находится в открытом доступе, исходный код проекта <a href='https://github.com/zak427zak/reciklomat_checker_telegram_bot'>на GitHub</a>"))
    else:
        return not_found(_l("Пользователя не существует! Попробуйте ещё раз или вернитесь позже!"))


@app.route('/user/language', methods=['POST'])
def user_set_language():
    payload = request.get_json() or request.form
    check_user = user_repo.get_by_telegram_id(payload['telegram_id'])

    if check_user:
        user_repo.update_language(check_user.id, payload['language'])
        record_a_visit(check_user)
        # login_user(check_user, True)
        return jsonify({'result': _l("Язык успешно изменен")})
    else:
        return not_found('Не можем найти вас в системе. Напишите что-нибудь боту, чтобы он авторизовал вас')


# Пример использования репозитория для подписки
@app.route('/user/subscribe', methods=['POST'])
def subscribe_user():
    payload = request.get_json() or request.form
    check_user = user_repo.get_by_telegram_id(payload['telegram_id'])
    if check_user:
        record_a_visit(check_user)
        subscription_repo.add_or_remove_subscription(check_user.id, payload['address'])
        return 'ok'
    else:
        return not_found("Пользователь не найден")


# Функция записи посещения
def record_a_visit(user):
    user_repo.update_last_seen(user.id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

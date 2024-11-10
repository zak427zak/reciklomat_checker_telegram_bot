from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):

    def update_subscription_status(self, user_id: int, is_telegram_on: bool):
        """
        Обновляет статус подписки на уведомления через Telegram.
        :param user_id: Идентификатор пользователя
        :param is_telegram_on: Новый статус подписки
        :return: Обновленный пользователь
        """
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            user.is_telegram_on = is_telegram_on
            self.session.commit()
        return user

    def update_language(self, telegram_id: str, language: str):
        """
        Обновляет язык пользователя по telegram_id и обновляет поле last_seen.
        :param telegram_id: Идентификатор пользователя в Telegram
        :param language: Новый язык пользователя
        :return: Объект User или None, если пользователь не найден
        """
        user = self.session.query(User).filter(User.id == telegram_id).first()
        if user:
            user.language = language
            user.last_seen = datetime.utcnow() + timedelta(hours=3)
            self.session.commit()
        return user

    def get_by_telegram_id(self, telegram_id):
        """
        Получение пользователя по telegram_id
        :param telegram_id: Идентификатор пользователя в Telegram
        :return: Объект User или None, если пользователь не найден
        """
        query = select(User).where(User.telegram_id == telegram_id)
        result = self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    def update_last_seen(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            user.last_seen = datetime.utcnow() + timedelta(hours=3)
            self.session.commit()
        return user

    def get_or_create_user(self, telegram_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None,
                           username: Optional[str] = None, registred_date: Optional[datetime] = None,
                           last_seen: Optional[datetime] = None, is_telegram_on: bool = False, language: str = "en"):
        """
        Creates or updates a new Reciklomat user in the database and returns the user object.
        """
        # Попытка найти пользователя по telegram_id
        existing_user = self.session.query(User).filter(User.telegram_id == telegram_id).first()

        if existing_user:
            # Если пользователь существует, обновить его данные
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.username = username
            existing_user.last_seen = last_seen or datetime.utcnow()
            existing_user.is_telegram_on = is_telegram_on
            existing_user.language = language  # Обновляем поле language
            self.session.commit()
            return existing_user
        else:
            # Если пользователь не найден, создаем нового
            new_user = User(telegram_id=telegram_id, first_name=first_name, last_name=last_name, username=username,
                            registred_date=registred_date or datetime.utcnow(),
                            last_seen=last_seen or datetime.utcnow(), is_telegram_on=is_telegram_on, language=language)
            self.session.add(new_user)
            self.session.commit()
            return new_user

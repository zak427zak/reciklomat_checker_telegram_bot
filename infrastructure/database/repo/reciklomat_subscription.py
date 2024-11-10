from sqlalchemy import select

from infrastructure.database.models import ReciklomatSubscription
from infrastructure.database.repo.base import BaseRepo


class ReciklomatSubscriptionRepo(BaseRepo):

    def get_by_user_id(self, user_id: int):
        """
        Получение всех подписок пользователя по его user_id
        """
        return self.session.query(ReciklomatSubscription).filter_by(user_id=user_id).all()

    def check_user_subscription(self, user_id: int, reciklomat_address: str):
        """
        Проверка, подписан ли пользователь на рецикломат по его адресу
        :param user_id: Идентификатор пользователя
        :param reciklomat_address: Адрес рецикломата
        :return: True, если подписка существует, иначе False
        """
        subscription = self.session.query(ReciklomatSubscription).filter_by(user_id=user_id,
                                                                            reciklomat_address=reciklomat_address).first()
        return bool(subscription)

    def get_by_address(self, address: str):
        query = select(ReciklomatSubscription).where(ReciklomatSubscription.reciklomat_address == address)
        result = self.session.execute(query)
        return result.scalars().all()

    def add_or_remove_subscription(self, user_id: int, reciklomat_address: str):
        existing_subscription = self.session.query(ReciklomatSubscription).filter_by(user_id=user_id,
                                                                                     reciklomat_address=reciklomat_address).first()

        if existing_subscription:
            self.session.delete(existing_subscription)
        else:
            new_subscription = ReciklomatSubscription(user_id=user_id, reciklomat_address=reciklomat_address)
            self.session.add(new_subscription)
        self.session.commit()

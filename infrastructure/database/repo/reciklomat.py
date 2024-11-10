from datetime import datetime, timedelta

from sqlalchemy import select

from infrastructure.database.models import Reciklomat, ReciklomatSubscription
from infrastructure.database.repo.base import BaseRepo


class ReciklomatRepo(BaseRepo):

    def get_all_sorted_by_status_and_occupancy(self):
        """
        Получение всех рецикломатов, отсортированных по статусу (в убывающем порядке) и по заполняемости (в порядке возрастания)
        """
        return self.session.query(Reciklomat).order_by(Reciklomat.status.desc(), Reciklomat.occupancy.asc()).all()

    def get_by_address(self, address: str):
        """
        Получение рецикломата по адресу
        """
        query = select(Reciklomat).where(Reciklomat.address == address)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def add_new_reciklomat(self, address: str, status: str, occupancy: float, capacity: float, lat: float, lon: float,
                           city: str, district: str):
        """
        Добавление нового рецикломата
        """
        new_reciklomat = Reciklomat(address=address, status=status, occupancy=occupancy, capacity=capacity, lat=lat,
                                    lon=lon, city=city, district=district,
                                    last_check=datetime.utcnow() + timedelta(hours=3))
        self.session.add(new_reciklomat)
        self.session.commit()
        return new_reciklomat

    def update_status_by_address(self, address: str, status: str, occupancy: float, capacity: float,
                                 last_check: datetime):
        """
        Обновление статуса рецикломата по адресу
        """
        reciklomat = self.get_by_address(address)
        if reciklomat:
            reciklomat.status = status
            reciklomat.occupancy = occupancy
            reciklomat.capacity = capacity
            reciklomat.last_check = last_check
            self.session.commit()

    def is_user_subscribed_to_reciklomat(self, user_id: int, reciklomat_address: str):
        """
        Проверяет, подписан ли пользователь на рецикломат по адресу.
        """
        return self.session.query(ReciklomatSubscription).filter_by(user_id=user_id,
                                                                    reciklomat_address=reciklomat_address).first() is not None

    def to_collection_reciklomats(self, page: int, per_page: int, current_user):
        """
        Преобразует результат запроса в список словарей с поддержкой пагинации, с учетом подписок пользователя
        """
        # Получение всех рецикломатов
        all_reciklomats = self.get_all_sorted_by_status_and_occupancy()

        # Кастомная пагинация
        offset = (page - 1) * per_page
        resources = all_reciklomats[offset:offset + per_page]

        # Преобразование в словари с учетом подписок пользователя
        data = []
        for reciklomat in resources:
            is_checked = self.is_user_subscribed_to_reciklomat(current_user.id, reciklomat.address)
            checked_data = "✅" if is_checked else "⛔"
            data.append({'id': reciklomat.id, 'address': reciklomat.address, 'is_checked': is_checked,
                'checked_data': checked_data})

        return data

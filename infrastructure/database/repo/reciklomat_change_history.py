from datetime import timedelta, datetime

from infrastructure.database.models import ReciklomatChangeHistory
from infrastructure.database.repo.base import BaseRepo


class ReciklomatChangeHistoryRepo(BaseRepo):

    def write_status_change(self, reciklomat_id: int, old_status: str, new_status: str):
        change_entry = ReciklomatChangeHistory(reciklomat_id=reciklomat_id, old_status=old_status,
            new_status=new_status, change_date=datetime.utcnow() + timedelta(hours=3))
        self.session.add(change_entry)
        self.session.commit()

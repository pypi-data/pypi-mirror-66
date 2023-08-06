from gwlib.base.base_service import BaseService
from gwlib.dao import BaseAlertDAO


class BaseAlertService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseAlertDAO()

    def get_by_alert_id(self, alert_id):
        return self.dao.get(alert_id=alert_id).to_json()

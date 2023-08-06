from gwlib.base.base_dao import BaseDAO
from gwlib.models import Alert


class BaseAlertDAO(BaseDAO):
    model = Alert

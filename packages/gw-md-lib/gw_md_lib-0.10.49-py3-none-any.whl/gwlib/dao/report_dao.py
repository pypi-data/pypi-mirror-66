from gwlib.base.base_dao import BaseDAO
from gwlib.models import Report


class BaseReportDAO(BaseDAO):
    model = Report

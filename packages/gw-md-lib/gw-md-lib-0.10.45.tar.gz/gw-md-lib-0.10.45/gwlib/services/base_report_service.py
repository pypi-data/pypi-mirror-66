from gwlib.base.base_service import BaseService
from gwlib.dao import BaseReportDAO


class BaseReportService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseReportDAO()

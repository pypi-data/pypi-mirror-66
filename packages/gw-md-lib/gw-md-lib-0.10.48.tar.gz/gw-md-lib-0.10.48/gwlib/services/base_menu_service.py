from gwlib.base.base_service import BaseService
from gwlib.dao import BaseMenuDAO
from gwlib.services import BaseUserService


class BaseMenuService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseMenuDAO()

    def get_user_menu(self, user_id):
        user_service = BaseUserService()
        return user_service.get_menu(user_id=user_id)

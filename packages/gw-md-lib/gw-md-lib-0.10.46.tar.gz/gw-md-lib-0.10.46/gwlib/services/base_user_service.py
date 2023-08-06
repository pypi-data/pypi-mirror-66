from gwlib.dao import BaseUserDAO
from gwlib.base.base_service import BaseService
from gwlib.models import User
from gwlib.models import UserType


class BaseUserService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseUserDAO()

    def get_by_user_id(self, user_id):
        return self.dao.get(user_id=user_id)

    def get_by_username(self, username):
        return self.dao.get(username=username)

    def get_menu(self, user_id):
        user = self.dao.get(user_id=user_id)  # type: User
        user_type = user.user_type  # type: UserType
        return user_type.menus

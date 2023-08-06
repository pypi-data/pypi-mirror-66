from sqlalchemy.orm import relationship

from . import db
from gwlib.models.user_type_menu import user_type_menu
from .model_json import ModelJson


class UserType(db.Model, ModelJson):
    __tablename__ = "gw_user_type"

    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)

    users = relationship("User", back_populates="user_type")
    user_types_policies = relationship("UserTypePolicy", lazy='dynamic')
    menus = db.relationship(
        "Menu",
        secondary=user_type_menu,
        passive_deletes=True,
        backref="user_menus")
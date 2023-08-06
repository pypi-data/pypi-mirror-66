from sqlalchemy import Table

from . import db

user_type_menu = Table('gw_user_type_menu',
                       db.Model.metadata,
                       db.Column('menu_id', db.Integer, db.ForeignKey('gw_menu.menu_id'), nullable=False),
                       db.Column('type_id', db.Integer, db.ForeignKey('gw_user_type.type_id'), nullable=False),
                       db.Column('deleted', db.Boolean, default=False, nullable=False)
                       )

from sqlalchemy import func

from gwlib.models import db, ModelJson


class Menu(db.Model, ModelJson):
    __tablename__ = "gw_menu"

    menu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    path = db.Column(db.String(80))
    menu_icon = db.Column(db.String(50))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

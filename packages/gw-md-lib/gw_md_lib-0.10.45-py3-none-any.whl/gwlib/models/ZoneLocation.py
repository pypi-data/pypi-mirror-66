from sqlalchemy import func
from sqlalchemy.orm import relationship

from gwlib.models import ModelJson
from . import db


class ZoneLocation(db.Model, ModelJson):
    __tablename__ = "gw_zone_location"

    location_id = db.Column(db.Integer, primary_key=True)
    hole_type_id = db.Column(db.Integer, db.ForeignKey('gw_zone.zone_id'), nullable=False)
    code = db.Column(db.String(length=45), nullable=True)
    alias = db.Column(db.String(length=45), nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)


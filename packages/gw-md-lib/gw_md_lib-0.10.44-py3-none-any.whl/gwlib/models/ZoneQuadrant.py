from sqlalchemy import func

from gwlib.models import ModelJson
from . import db


class ZoneQuadrant(db.Model, ModelJson):
    __tablename__ = "gw_zone_quadrant"

    quadrant_id = db.Column(db.Integer, primary_key=True)
    hole_type_id = db.Column(db.Integer, db.ForeignKey('gw_zone.zone_id'), nullable=False)
    code = db.Column(db.String(length=3), nullable=True)
    quadrant = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)


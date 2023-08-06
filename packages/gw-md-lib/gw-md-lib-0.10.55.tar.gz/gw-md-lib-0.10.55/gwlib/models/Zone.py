from sqlalchemy import func

from gwlib.models import ModelJson
from . import db


class Zone(db.Model, ModelJson):
    __tablename__ = "gw_zone"

    zone_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('gw_golf_course.course_id'), nullable=False)
    code = db.Column(db.String(length=3), nullable=True)
    alias = db.Column(db.String(length=45), nullable=False)
    note_required = db.Column(db.Boolean, default=False, nullable=False)
    hole_linked = db.Column(db.Boolean, default=False, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)


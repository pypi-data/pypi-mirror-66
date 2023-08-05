from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .Alert import *
from .GolfCourse import *
from .User import *
from .Hole import *
from .Sensor import *
from .Report import *
from .UserType import *
from .UserToken import *
from .UserTypePolicy import *
from .Resource import *
from .Zone import *
from .menu import Menu

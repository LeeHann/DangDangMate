from flask import Blueprint
routes = Blueprint('routes', __name__)

from .users import *
from .main import *
from .mypage import *
from .posting import *
from .review import *

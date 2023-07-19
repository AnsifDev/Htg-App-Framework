from .py.Activity import Activity
from .py.Application import Application
from .py.SubActivity import SubActivity
from .py.ComponentManager import ComponentManager

from gi.repository import Adw
def get_default_application() -> Application: return Adw.Application.get_default()
from .py.Activity import Activity
from .py.Application import Application
from .py.DialogActivity import DialogActivity
from .py.ComponentManager import ComponentManager
from .py.ActivityFragment import ActivityFragment

from gi.repository import Adw
def get_default_application() -> Application: return Adw.Application.get_default()
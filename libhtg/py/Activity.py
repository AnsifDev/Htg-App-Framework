import Htg
from os import path

class Activity:
    __content = None
    __window_close_request_handler = None
    
    def _set_content(self, filename: str, id: str = None):
        from .Application import Application
        ui_file_path = path.join("ui", filename)
        self.__builder, self.__content = Htg.get_default_application()._build_ui(ui_file_path, id)

    def _get_content(self): return self.__content

    def _get_window(self):
        from .Application import Application 
        return Htg.get_default_application()._win

    def _finish(self): 
        from .Application import Application
        Htg.get_default_application()._get_component_manager()._end_activity(self)
    
    def find_view_by_id(self, id: str): return self.__builder.get_object(id)
    
    def _on_create(self): pass

    def _on_started(self, *args): self.__window_close_request_handler = self._get_window().connect("close-request", self._on_window_closing)

    def _on_stopped(self): self._get_window().disconnect(self.__window_close_request_handler)

    def _on_destroy(self): pass

    def _on_sub_activity_returns(self, request: int, *responses): pass

    def _on_window_closing(self, window) -> bool: return False
    
import os, Htg

class SubActivity:
    def _get_window(self): return Htg.get_default_application()._get_component_manager()._get_sub_activity_window(self)

    def _set_content(self, filename: str, id: str = None):
        ui_file_path = os.path.join("ui", filename)
        self.__builder, self.__content = Htg.get_default_application()._build_ui(ui_file_path, id)

    def _get_content(self): return self.__content

    def _finish(self, *responses): Htg.get_default_application()._get_component_manager()._end_sub_activity(self, *responses)
    
    def find_view_by_id(self, id: str): return self.__builder.get_object(id)
    
    def _on_create(self, *args): 
        self._get_window().connect("close-request", self._on_window_closing)

    def _on_destroy(self): pass

    def _on_sub_activity_returns(self, request: int, *responses): pass

    def _on_window_closing(self, window) -> bool: 
        self._finish()
        return False

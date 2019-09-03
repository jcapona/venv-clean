from asciimatics.widgets import Frame, Layout, Button, CheckBox, Label
from asciimatics.exceptions import StopApplication
from venv_clean.core.utils import find_virtualenvs, delete_folder


class VenvView(Frame):
    def __init__(self, screen, path):
        super(VenvView, self).__init__(screen,
                                       screen.height,
                                       screen.width,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Virtual Environment List")

        self.path = path
        self.venvs = self.__find_venvs(self.path)

        self.layout_main = Layout([80, 20], fill_frame=True)
        self.add_layout(self.layout_main)

        self.layout_bottom = Layout([1, 1])
        self.add_layout(self.layout_bottom)

        self.layout_bottom.add_widget(Button("Delete", self._delete), 0)
        self.layout_bottom.add_widget(Button("Quit", self._quit), 1)

        self.__draw()
        self.fix()
        self.selected_size = 0

    def __draw(self):
        self.layout_main.clear_widgets()
        self.layout_main.reset()

        self.layout_main.add_widget(Label('Path'), 0)
        self.layout_main.add_widget(Label('Size MB'), 1)

        for v in self.venvs:
            self.layout_main.add_widget(v['checkbox'], 0)
            self.layout_main.add_widget(Label(str(v['size'])), 1)

    def _reload_items(self):
        self.venvs = self.__find_venvs(self.path)
        self.selected_size = 0
        self.reset()
        self.__draw()
        self.fix()

    def __calculate_selected_size(self):
        for v in self.venvs:
            if v['checkbox'].value:
                self.selected_size += float(v['size'])

    def _delete(self):
        for v in self.venvs:
            if v['checkbox'].value:
                delete_folder(v['location'])
        self._reload_items()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

    def __find_venvs(self, path):
        venvs = find_virtualenvs(path)
        for v in venvs:
            v['checkbox'] = CheckBox(v['location'],
                                     on_change=self.__calculate_selected_size)
        return venvs



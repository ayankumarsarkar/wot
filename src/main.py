import toga
from toga.constants import COLUMN

import re
from pathlib import Path

class WOT(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()
        self.text_input = toga.MultilineTextInput()

        box             = toga.Box(direction=COLUMN, margin=5)
        paths_box       = toga.Box(direction=COLUMN, margin=5)
        projects_box    = toga.Box(direction=COLUMN, margin=5)

        active_path     = 'C:/Users/Admin/Desktop'
        archive_path    = 'C:/Users/Admin/Documents'

        topic_code_pattern = re.compile(r'^[A-Z]{3}-')

        active_label    = toga.Label(text='Active Projects Path: {}'.format(active_path))
        archive_label   = toga.Label(text='Archived Projects Path: {}'.format(archive_path))

        paths_box.add(active_label)
        paths_box.add(archive_label)

        project_list    = [path.name for path in Path(archive_path).iterdir() if path.is_dir and topic_code_pattern.match(path.name)]

        for project in project_list:
            label = toga.Label(text=project)
            projects_box.add(label)
        
        box.add(paths_box)
        box.add(projects_box)

        self.main_window.content = box
        self.main_window.show()

def main():
    return WOT("Worflow Organising Tool", "in.new.wot")

if __name__ == "__main__":
    main().main_loop()

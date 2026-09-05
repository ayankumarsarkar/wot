import toga
from toga.constants import COLUMN

import re
from pathlib        import Path

import os

active_path         = r'C:/Users/Admin/Desktop'
archive_path        = r'C:/Users/Admin/Documents'
archive_remote_path = r'H:/My Drive/2. Secondary - Fictions'

project_list = []

def open_folder(widget):
    project_dictionary = [p for p in project_list if 'name' in p and p.get('name') == widget.text]

    if project_dictionary[0].get('type') == 'local':
        project_location = f'{archive_path}/{widget.text}'
        print(f"Fine, let's see {(project_location)}.")
        os.startfile(project_location)

    elif project_dictionary[0].get('type') == 'remote':
        project_location = f'{archive_remote_path}/{widget.text}'
        print(f"ugh, alright, let's go to {(project_location)}.")
        os.startfile(project_location)

    else:
        print(f"Eww, I won't go to {widget.text}!")

class WOT(toga.App):
    def startup(self):
        self.main_window    = toga.MainWindow()
        self.text_input     = toga.MultilineTextInput()

        box             = toga.Box(direction=COLUMN, margin=5)
        paths_box       = toga.Box(direction=COLUMN, margin=5)
        projects_box    = toga.Box(direction=COLUMN, margin=5)

        topic_code_pattern = re.compile(r'^[A-Z]{3}-')

        active_label            = toga.Label(text='Active Projects Path: {}'.format(active_path))
        archive_label           = toga.Label(text='Archived Projects Path: {}'.format(archive_path))
        archive_remote_label    = toga.Label(text='Remote Archive Projects Paths: {}'.format(archive_remote_path))

        paths_box.add(active_label)
        paths_box.add(archive_label)
        paths_box.add(archive_remote_label)

        # Adding local projects
        for path in Path(archive_path).iterdir():
            if path.is_dir and topic_code_pattern.match(path.name):
                project_data = {
                    'name': path.name,
                    'type': 'local'
                }
                project_list.append(project_data)

        # Adding remote projects
        for path in Path(archive_remote_path).iterdir():
            if path.is_dir and topic_code_pattern.match(path.name):
                project_data = {
                    'name': path.name,
                    'type': 'remote'
                }
                project_list.append(project_data)

        for project in project_list:
            project_box = toga.Box()
            project_name = toga.Button(
                text=f'{project['name']}', 
                id=f'{project['name']}_project',
                on_press=open_folder,
                direction=COLUMN
            )
            project_type    = toga.Label(text=f'{project['type']}')

            project_box.add(project_name, project_type)
            projects_box.add(project_box)

        box.add(paths_box)
        box.add(projects_box)

        self.main_window.content = box
        self.main_window.show()

def main():
    return WOT("Worflow Organising Tool", "in.new.wot")

if __name__ == "__main__":
    main().main_loop()

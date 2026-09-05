import toga
from toga.constants import COLUMN

import re
from pathlib        import Path

import os

active_path         = r'C:/Users/Admin/Desktop'
archive_path        = r'C:/Users/Admin/Documents/Archive'
archive_remote_path = r'H:/My Drive/2. Secondary - Fictions'

project_list        = []
project_list_active = []

def make_active(widget):
    print('Huh, what do you want me to do?')

def show_list(widget):
    if isinstance(widget, str):
        print(f"You've sent me a string of... what? {widget}?")
        items = []
        for project in project_list:
            project_box             = toga.Box()
            project_type            = toga.Label(text=f'{project['type']}')
            project_state_button    = toga.Button(text='add to active', on_press=make_active)
            project_name            = toga.Button(
                                        text=f'{project['name']}',
                                        id=f'{project['name']}_project',
                                        on_press=open_folder, direction=COLUMN
                                    )
            project_box.add(project_name, project_type, project_state_button)
            items.append(project_box)
        return items
    else:
        print(f"Here we go, some proper widgetty string of letters! \n {widget.text}")
        if widget.text == 'Active':
            print('These are currently active projects.')

        elif widget.text == 'Inactive':
            print('You should really consider finishing some of them.')

        elif widget.text == 'All Projects':
            print('Here are all your projects.')

        else:
            print('This is unexpected...')

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

        tabs_box                = toga.Box()
        all_projects_tab        = toga.Button(text='All Projects', on_press=show_list)
        active_projects_tab     = toga.Button(text='Active', on_press=show_list)
        inactive_projects_tab   = toga.Button(text='Inactive', on_press=show_list)

        tabs_box.add(all_projects_tab, active_projects_tab, inactive_projects_tab)

        active_label            = toga.Label(text=f'Active Projects Path: {active_path}')
        archive_label           = toga.Label(text=f'Archived Projects Path: {archive_path}')
        archive_remote_label    = toga.Label(text=f'Remote Archive Projects Paths: {archive_remote_path}')

        paths_box.add(active_label)
        paths_box.add(archive_label)
        paths_box.add(archive_remote_label)

        topic_code_pattern = re.compile(r'^[A-Z]{3}-')

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

        list_items = show_list('All Projects')

        projects_box.add(*list_items)

        box.add(tabs_box)
        box.add(paths_box)
        box.add(projects_box)

        self.main_window.content = box
        self.main_window.show()

def main():
    return WOT("Workflow Organising Tool", "in.new.cube")

if __name__ == "__main__":
    main().main_loop()

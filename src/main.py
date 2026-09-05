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

def make_active(widget):
    print('Huh, what do you want me to do?')

#def show_list(widget):
#   if widget.text == 'Active':
#       print('These are currently active projects.')
#   elif widget.text == 'Inactive':
#       print('You should really consider finishing some of them.')
#   elif widget.text == 'All Projects':
#       print('Here are all your projects.')
#   else:
#       print('This is unexpected...')

def open_folder(widget, row):
    project_name        = row.name
    project_dictionary  = [p for p in project_list if 'name' in p and p.get('name') == project_name]

    if project_dictionary[0].get('type') == 'local':
        project_location = f'{archive_path}/{project_name}'
        print(f"Fine, let's see {(project_location)}.")
        os.startfile(project_location)

    elif project_dictionary[0].get('type') == 'remote':
        project_location = f'{archive_remote_path}/{project_name}'
        print(f"ugh, alright, let's go to {(project_location)}.")
        os.startfile(project_location)

    else:
        print(f"Eww, I won't go to {project_name}!")

class WOT(toga.App):
    def startup(self):
        box             = toga.Box(direction=COLUMN, margin=5)
        paths_box       = toga.Box(direction=COLUMN, margin=5)

        #tab_container           = toga.OptionContainer(flex=1)
        #tabs_box                = toga.Box()
        #all_projects_tab        = toga.Button(text='All Projects', on_press=show_list)
        #active_projects_tab     = toga.Button(text='Active', on_press=show_list)
        #inactive_projects_tab   = toga.Button(text='Inactive', on_press=show_list)

        #tabs_box.add(all_projects_tab, active_projects_tab, inactive_projects_tab)
        #tab_container.content.append(tabs_box)

        active_label            = toga.Label(text=f'Active Projects Path: {active_path}')
        archive_label           = toga.Label(text=f'Archived Projects Path: {archive_path}')
        archive_remote_label    = toga.Label(text=f'Remote Archive Projects Paths: {archive_remote_path}')

        paths_box.add(active_label)
        paths_box.add(archive_label)
        paths_box.add(archive_remote_label)

        project_table = toga.Table(
            columns     = ['Project Name', 'Location'],
            accessors   = ['name', 'type'],
            data=project_list,
            on_activate=open_folder,
            flex=1
        )

        box.add(
            #tabs_box,
            paths_box, 
            project_table
        )

        self.main_window = toga.MainWindow(content=box).show()

def main():
    return WOT("Workflow Organising Tool", "in.new.cube")

if __name__ == "__main__":
    main().main_loop()

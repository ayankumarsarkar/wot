import os
import re
import sys
import toga
from toga.constants import COLUMN, CENTER as CENTRE
from pathlib        import Path

active_path             = r'C:/Users/Admin/Desktop'
archive_path            = r'C:/Users/Admin/Documents/Archive'
archive_remote_path     = r'H:/My Drive/2. Secondary - Fictions'

project_list            = []
project_list_active     = [
    { 'name': 'WOT-Workflow Organising Tool', 'type': 'local'},
    #{ 'name': '', 'type': 'local'},
]
project_list_inactive   = []

topic_code_pattern      = re.compile(r'^[A-Z]{3}-')
# Also add a pattern for eliminating .lnk files

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

# Making list of inactive projects
project_list_inactive.extend([d for d in project_list if d not in project_list_active])

def system_theming(table1, table2, table3):
    if sys.platform == 'win32':
        table1._impl.native.Columns[0].Width = -1
        table2._impl.native.Columns[0].Width = -1
        table3._impl.native.Columns[0].Width = -1

def make_active(widget):
    print('Huh, what do you want me to do?')

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
        tabs_container  = toga.OptionContainer(flex=1)

        # Make these Paths editable
        active_label            = toga.Label(text=f'Active Projects Path: {active_path}')
        archive_label           = toga.Label(text=f'Archived Projects Path: {archive_path}')
        archive_remote_label    = toga.Label(text=f'Remote Archive Projects Paths: {archive_remote_path}')

        paths_box.add(active_label)
        paths_box.add(archive_label)
        paths_box.add(archive_remote_label)

        all_project_tab        = toga.Box(
            direction=COLUMN,
            padding=20,
            align_items=CENTRE
        )
        active_project_tab     = toga.Box(
            direction=COLUMN,
            padding=20,
            align_items=CENTRE
        )
        inactive_project_tab   = toga.Box(
            direction=COLUMN,
            padding=20,
            align_items=CENTRE
        )

        all_project_table = toga.Table(
            columns     = ['Project Name', 'Location'],
            accessors   = ['name', 'type'],
            data        = project_list,
            on_activate = open_folder,
            flex        = 1
        )
        active_project_table = toga.Table(
            columns     = ['Project Name', 'Location'],
            accessors   = ['name', 'type'],
            data        = project_list_active,
            on_activate = open_folder,
            flex        = 1
        )
        inactive_project_table = toga.Table(
            columns     = ['Project Name', 'Location'],
            accessors   = ['name', 'type'],
            data        = project_list_inactive,
            on_activate = open_folder,
            flex        = 1
        )

    # A width of -1 auto-resizes the column to fit the longest item in it

        all_project_tab.add(all_project_table)
        active_project_tab.add(active_project_table)
        inactive_project_tab.add(inactive_project_table)

        tabs_container.content.append('All Projects', all_project_tab)
        tabs_container.content.append('Active', active_project_tab)
        tabs_container.content.append('Inactive', inactive_project_tab)

        box.add(
            paths_box, 
            tabs_container
        )

        self.main_window = toga.MainWindow(content=box).show()
        system_theming(all_project_table, active_project_table, inactive_project_table)

def main():
    return WOT("Workflow Organising Tool", "in.new.cube")

if __name__ == "__main__":
    main().main_loop()

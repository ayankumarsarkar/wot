import os
import re
import sys
import toga
from toga.constants import COLUMN, ROW, CENTER as CENTRE
from pathlib        import Path
import tomlkit

with open('src/config.toml', 'rb') as f:
    config = tomlkit.load(f)

active_path             = config['paths']['active_path']
archive_path            = config['paths']['archive_path']
archive_remote_path     = config['paths']['archive_remote_path']

project_list            = []
project_list_active     = []
project_list_inactive   = []

def gather_projects(_path: Path, _type: str, _pattern, _project_list: list):
    if _path.is_dir and _pattern.match(_path.name):
        _project_data = { 'name': _path.name, 'type': _type }
        return _project_list.append(_project_data)

topic_code_pattern0     = re.compile(r'^[A-Z]{3}-')
# Also add a pattern for eliminating .lnk files

# Adds local projects
for path in Path(archive_path).iterdir():
    gather_projects(path, 'local', topic_code_pattern0, project_list)

# Adds remote projects
for path in Path(archive_remote_path).iterdir():
    gather_projects(path, 'remote', topic_code_pattern0, project_list)

# Makes a list of active projects
lnk_names = {
    path.stem.lower().strip() for path in Path(active_path).glob('*.lnk')
}

for entry in project_list:
    name = entry.get('name', '')
    topic_code_pattern1 = re.findall(r'^[A-Z]{3}', name)
    
    first_3_words = ''.join(topic_code_pattern1[:3]).lower()
    
    if first_3_words in lnk_names:
        project_list_active.append(entry)

# Makes list of inactive projects
project_list_inactive.extend([
    d for d in project_list if d not in project_list_active
])

def system_theming(table1, table2, table3):
    # A width of -1 auto-resizes the column to fit the longest item in it
    if sys.platform == 'win32':
        table1._impl.native.Columns[0].Width = -1
        table2._impl.native.Columns[0].Width = -1
        table3._impl.native.Columns[0].Width = -1

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

        create_new_project_button = toga.Button(text='New', on_press=self.create_new_project)
        edit_project_paths_button = toga.Button(text='Edit', on_press=self.edit_paths)
        buttons = toga.Box(children=[
            create_new_project_button,
            edit_project_paths_button
        ], direction=ROW)

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
        # Add a way of refreshing the lists/tables

        all_project_tab.add(all_project_table)
        active_project_tab.add(active_project_table)
        inactive_project_tab.add(inactive_project_table)

        tabs_container.content.append('All Projects', all_project_tab)
        tabs_container.content.append('Active', active_project_tab)
        tabs_container.content.append('Inactive', inactive_project_tab)

        box.add(
            paths_box, 
            buttons, 
            tabs_container
        )

        self.main_window = toga.MainWindow(content=box).show()
        system_theming(all_project_table, active_project_table, inactive_project_table)

    def create_new_project(self, widget):
        self.title_input = toga.TextInput(placeholder='Title', padding=(0, 0, 10, 0), flex=1)
        row_title   = toga.Box(children=[self.title_input], direction=ROW)

        self.code_input      = toga.TextInput(placeholder='Code', padding=(0, 5, 10, 0), flex=1)
        location_input  = toga.TextInput(placeholder='Location', padding=(0, 0, 10, 5), flex=1)
        row_inputs      = toga.Box(children=[self.code_input, location_input], direction=ROW)

        cancel_button   = toga.Button('Cancel', on_press=self.close_dialogue, padding=(0, 5, 0, 0), flex=1)
        create_button   = toga.Button('Create', on_press=self.create_handler, padding=(0, 0, 0, 5), flex=1)
        row_buttons     = toga.Box(children=[cancel_button, create_button], direction=ROW)

        dialogue_container = toga.Box(children=[row_title, row_inputs, row_buttons], direction=COLUMN, padding=20)

        self.new_window = toga.Window(title='New Project', size=(260, 140))
        self.new_window.content = dialogue_container
        self.new_window.show()

    def close_dialogue(self, widget):
        self.new_window.close()

    def create_handler(self, widget):
        title = self.title_input.value
        code = self.code_input.value.strip()

        if not title or not code:
            print('Huh, what do you want me to do?')
            self.new_window.error_dialog('Missing Information', 'Huh, what do you want me to do?')
            return

        try:
            archive_dir     = Path(archive_path)
            project_name    = f'{code}-{title}'
            target_path     = archive_dir/project_name

            target_path.mkdir(parents=True, exist_ok=False)

            self.new_window.info_dialog("Success", f"Created project:\n{target_path}")
            self.new_window.close()
            
        except FileExistsError:
            self.new_window.error_dialog("Error", f"The project '{project_name}' already exists at this location.")
        except PermissionError:
            self.new_window.error_dialog("Error", "You do not have permission to create a project here.")
        except Exception as e:
            self.new_window.error_dialog("Error", f"Failed to create project:\n{str(e)}")

    def edit_paths(self, widget):
        active_path_label   = toga.Label(text='Active Path:')
        active_path_input   = toga.TextInput(
            placeholder=config['paths']['active_path'],
            flex=1
        )
        active_path_box     = toga.Box(children=[
            active_path_label, active_path_input
        ], direction=ROW)

        archive_path_label  = toga.Label(text='Active Path:')
        archive_path_input  = toga.TextInput(
            placeholder=config['paths']['archive_path'],
            flex=1
        )
        archive_path_box    = toga.Box(children=[
            archive_path_label, archive_path_input
        ], direction=ROW)

        archive_remote_path_label   = toga.Label(text='Active Path:')
        archive_remote_path_input   = toga.TextInput(
            placeholder=config['paths']['archive_remote_path'],
            flex=1
        )
        archive_remote_path_box     = toga.Box(children=[
            archive_remote_path_label, archive_remote_path_input
        ], direction=ROW)

        def save_paths(widget):
            path1 = active_path_input.value
            path2 = archive_path_input.value
            path3 = archive_remote_path_input.value

            print('Save button pressed')
            if path1 != '' and Path(path1).exists():
                print('All is well... value is not empty')
                config['paths']['active_path'] = path1

            if path2 != '' and Path(path2).exists():
                print('All is well... value is not empty')
                config['paths']['active_path'] = path2

            if path3 != '' and Path(path3).exists():
                print('All is well... value is not empty')
                config['paths']['active_path'] = path3

            with open('src/config.toml', 'w', encoding='utf-8') as f:
                tomlkit.dump(config, f)

        save_button = toga.Button(text='Save', on_press=save_paths)

        input_box                   = toga.Box(children=[
            active_path_box,
            archive_path_box,
            archive_remote_path_box,
            save_button
        ], direction=COLUMN)

        self.path_editor = toga.Window(title='Edit Paths', size=(260, 140))
        self.path_editor.content = input_box
        self.path_editor.show()

def main():
    return WOT("Workflow Organising Tool", "in.new.cube")

if __name__ == "__main__":
    main().main_loop()

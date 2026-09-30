import pylnk3
#from pathlib import Path

def create(file_path: str, lnk_name: str, file_description: str):
  # Creates a shortcut pointing to notepad.exe
  pylnk3.for_file(
    target_file = file_path,
    lnk_name    = lnk_name,
    description = file_description
  )
  
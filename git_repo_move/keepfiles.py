"""
"""

import os
import random

class KeepFiles():
    def __init__(self, files, directories, dir_structure_flat, working_dir="keep1234"):
        self.keep_files = files
        self.keep_directories = directories
        self.dir_structure_flat = dir_structure_flat
        self.working_dir = working_dir


    def generate_commands(self):
        dirnames = set({self.working_dir})
        mv_commands = []
        for file in self.keep_files:
            if self.dir_structure_flat:
                dest = os.path.join(self.working_dir, os.path.basename(file))
            else:
                dest = os.path.join(self.working_dir, file)
            dirnames.add(os.path.dirname(dest))
            mv_commands.append(f"mv {file} {dest}")

        for directory in self.keep_directories:
            if self.dir_structure_flat:
                source = os.path.join(directory, "*")
            else:
                source = directory
            mv_commands.append(f"mv {source} {self.working_dir}")

        mkdir_commands = []
        for directory in dirnames:
            mkdir_commands.append(f"mkdir -p {directory}")

        return mkdir_commands + mv_commands

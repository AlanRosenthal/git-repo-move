"""
Keep Files class
"""

import os
import random

class KeepFiles():
    """
    KeepFiles class. These are the files and directories you want to save
    """
    def __init__(self, keep_files, keep_directories, is_dir_structure_flat, final_directory):
        self.keep_files = keep_files
        self.keep_directories = keep_directories
        self.is_dir_structure_flat = is_dir_structure_flat
        # guaranteed to be unused by picking an idiotic directory name
        self._working_dir = "keep1234"
        self.final_directory = final_directory


    @property
    def working_dir(self):
        return self._working_dir


    def get_files_and_directories(self):
        """
        Return a list of files and directories
        """
        result = []
        if self.keep_files:
            result.extend(self.keep_files)
        if self.keep_directories:
            result.extend(self.keep_directories)
        return result


    def generate_commands(self):
        """
        Generate commands required for the Keep Stage
        """
        if self.final_directory:
            dest_base = os.path.join(self.working_dir, self.final_directory)
        else:
            dest_base = self.working_dir
        dirnames = set({dest_base})
        mv_commands = []

        # commands to move files
        for file in self.keep_files:
            if self.is_dir_structure_flat:
                dest = os.path.join(dest_base, os.path.basename(file))
            else:
                dest = os.path.join(dest_base, file)
            dirnames.add(os.path.dirname(dest))
            mv_commands.append(f"mv -f {file} {dest}")

        # commands to move directories
        for directory in self.keep_directories:
            if self.is_dir_structure_flat:
                source = os.path.join(directory, "*")
            else:
                source = directory
            mv_commands.append(f"mv -f {source} {dest_base}")

        mkdir_commands = []
        for directory in dirnames:
            mkdir_commands.append(f"mkdir -p {directory}")

        return sorted(mkdir_commands) + mv_commands

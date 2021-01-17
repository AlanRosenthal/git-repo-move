"""
Keep Files class
"""

import os
import random


class KeepFiles:
    """
    KeepFiles class. These are the files and directories you want to save
    """

    def __init__(
        self, keep_files, keep_directories, is_dir_structure_flat, final_directory
    ):
        self.keep_files = keep_files
        self.keep_directories = [os.path.normpath(x) for x in keep_directories]
        self.is_dir_structure_flat = is_dir_structure_flat
        # guaranteed to be unused by picking an idiotic directory name
        self._working_dir = "keep1234"
        self.final_directory = final_directory
        self._commands = []
        self.generate_commands()

    @property
    def working_dir(self):
        return self._working_dir

    @property
    def commands(self):
        return self._commands

    @property
    def common_path(self):
        """
        Return a common path (if any) for all files and directories
        """
        directories = []
        for file in self.keep_files:
            directories.append(os.path.dirname(file))
        if self.keep_directories:
            directories.extend(self.keep_directories)

        # special case: having only one directory will cause sadness.
        # it will result in `mv ./* folder` which will move the .git folder and :kaboom"
        if not self.keep_files and len(self.keep_directories) == 1:
            return os.path.dirname(self.keep_directories[0])

        return os.path.commonpath(directories)

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
        keep_files = [os.path.relpath(x, self.common_path) for x in self.keep_files]
        for file in keep_files:
            if self.is_dir_structure_flat:
                dest = os.path.join(dest_base, os.path.basename(file))
            else:
                dest = os.path.join(dest_base, self.common_path, file)
            dirnames.add(os.path.dirname(dest))
            mv_commands.append(f"mv -f {file} {dest}")

        # commands to move directories
        keep_directories = [
            os.path.relpath(x, self.common_path) for x in self.keep_directories
        ]
        for directory in keep_directories:
            dest = dest_base
            if self.is_dir_structure_flat:
                source = os.path.join(directory, "*")
            else:
                source = directory
                if self.common_path:
                    dest = os.path.join(dest_base, self.common_path)
            mv_commands.append(f"mv -f {source} {dest}")

        mkdir_commands = []
        for directory in dirnames:
            mkdir_commands.append(f"mkdir -p {directory}")

        self._commands = sorted(mkdir_commands) + mv_commands

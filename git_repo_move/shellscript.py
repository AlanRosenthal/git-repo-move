"""
Shell Script Class
"""

import os
import stat


class ShellScript():
    """
    """
    def __init__(self, keepfiles, gitinfo, save_shell_script, shell_script_name):
        self.keepfiles = keepfiles
        self.gitinfo = gitinfo
        self.save_shell_script = save_shell_script
        self.shell_script_name = shell_script_name
        self.script = []
        self.generate_script()
        if save_shell_script:
            self.save_script()

    def generate_script(self):
        self.script.append("#! /bin/env bash")
        self.script.append("")
        self.script.append("####################################################################")
        self.script.append("# This script was generated by git-repo-move! Star it on Github ⭐ #")
        self.script.append("####################################################################")
        self.script.append("")
        self.script.append("# Create a new branch (delete if exists)")
        self.script.append(self.gitinfo.create_new_branch_cmd())
        self.script.append("")
        self.script.append("# The tree-filter flag will run a command on every commit")
        self.script.append("# Let's run a command to move all the files we care about to a safe location")
        keepfiles_list = ", ".join(self.keepfiles.get_files_and_directories())
        self.script.append(f"# Move {keepfiles_list} to {self.keepfiles.working_dir}")
        keepfiles_cmds = "; \\ \n    ".join(self.keepfiles.commands)
        self.script.append(f"git filter-branch --force --prune-empty --tree-filter \"{keepfiles_cmds}\"")
        self.script.append("")
        self.script.append("# The subdirectory-filter flag filters everything not in the specified folder")
        self.script.append(f"git filter-branch --force --prune-empty --subdirectory-filter {self.keepfiles.working_dir}")
        self.script.append("")
        self.script.append("# Add a new remote and push the branch")
        self.script.append(self.gitinfo.add_new_remote_cmd())
        self.script.append(self.gitinfo.push_branch_to_remote_cmd())
        self.script.append("")
        self.script.append("# Let's remove the remote since we don't need it anymore")
        self.script.append(self.gitinfo.remove_new_remote_cmd())

    def save_script(self):
        with open(self.shell_script_name, "w") as file:
            for line in self.script:
                file.write(line)
                file.write("\n")

        # Mark the script as executable
        st = os.stat(self.shell_script_name)
        os.chmod(self.shell_script_name, st.st_mode | stat.S_IEXEC)


"""
CLI interface for git-repo-move
"""

import os
import sys
import click
from .keepfiles import KeepFiles
from .gitinfo import GitInfo
from .shellscript import ShellScript


@click.command()
@click.option("--file", multiple=True, help="Files to keep")
@click.option("--directory", multiple=True, help="Directories to keep")
@click.option(
    "--directory-structure",
    type=click.Choice(["FLAT", "ORIGINAL"], case_sensitive=False),
    required=True,
    help="Select the new directory structure",
)
@click.option("--final_directory", help="Move all kept files under this directory")
@click.option("--git-remote-url", help="URL of the new git repo", required=True)
@click.option("--git-branch", help="Git branch name", required=True)
@click.option(
    "--dont-save-shell-script",
    is_flag=True,
    default=False,
    help="Save the shell script to a file (recommended to document in PR)",
)
@click.option(
    "--shell-script-name", default="git-repo-move.sh", help="Name of the shell script"
)
@click.option(
    "--try-keep",
    is_flag=True,
    default=False,
    help="Test out the Keep stage (run outside of git)",
)
@click.option("--execute", is_flag=True, default=False, help="Run the shell script")
def main(
    file,
    directory,
    directory_structure,
    final_directory,
    git_remote_url,
    git_branch,
    dont_save_shell_script,
    shell_script_name,
    try_keep,
    execute,
):
    """
    This utility will help you move files from one git repo to another, while preserving history.
    Under the hood, this utility uses git-filter-branch, but the API is much more user friendly.

    \b
    Select what files/directories you want to keep
        Use --file and --dir to select what files you want moved
    Select the new directory for the files
        Use --final_directory to specify the new subdirectories for all kept files
        Use --dir-structure to specify if you want to keep the original directory str
            FLAT: flatten all the file into one directory
            ORIGINAL: preserve the original directory structure
    Select configuration options
        Use --git-remote, --git-branch, --dont-save-shell-script, --save-shell-script-name
        --try-keep, and --execute to configuration execution
    """
    gitinfo = GitInfo(remote_url=git_remote_url, branch=git_branch)
    keepfiles = KeepFiles(
        keep_files=file,
        keep_directories=directory,
        is_dir_structure_flat=directory_structure == "FLAT",
        final_directory=final_directory,
    )
    shellscript = ShellScript(
        keepfiles=keepfiles,
        gitinfo=gitinfo,
        save_shell_script=not dont_save_shell_script,
        shell_script_name=shell_script_name,
    )

    if try_keep:
        print(
            f"Running the keep script on this repo, run `git reset --hard && rm -rf {keepfiles.working_dir}` to undo everything"
        )
        print(f"Inspect the directory: {keepfiles.working_dir}")
        for cmd in keepfiles.commands:
            retval = os.system(cmd)
            if retval != 0:
                sys.exit(retval)
        sys.exit(0)

    if execute:
        sys.exit(shellscript.execute())

import click
from .keepfiles import KeepFiles


@click.command()
@click.option("--file", multiple=True, help="Files to keep")
@click.option("--directory", multiple=True, help="Directories to keep")
@click.option("--dir-structure", type=click.Choice(['FLAT', 'ORIGINAL'], case_sensitive=False), required=True, help="Select the new directory structure")
@click.option("--final-dir", default=".", help="Move all kept files under this directory")
@click.option("--git-remote", help="Remote of new repo")
@click.option("--git-branch", help="Git branch name")
@click.option("--save-shell-script", is_flag=True, default=True, help="Save the shell script to a file (recommended to document in PR)")
@click.option("--shell-script-name", default="gitmove.sh", help="Name of the shell script")
@click.option("--try-keep", is_flag=True, default=False, help="Test out the Keep stage (run outside of git)")
@click.option("--execute", is_flag=True, default=False, help="Run the shell script")
def main(file, directory, dir_structure, final_dir, git_remote, git_branch, save_shell_script, shell_script_name, try_keep, execute):
    """
    This utility will help you move files from one git repo to another, while preserving history.
    Under the hood, this utility uses git-filter-branch, but the API is much more user friendly.

    \b
    Stage 1: Select what files/directories you want to keep
        Use --file and --dir to select what files you want moved
        Use --dir-structure to specify if you want to keep the original directory str
            FLAT: flatten all the file into one directory
            ORIGINAL: preserve the original directory structure
    Stage 2: Select the new directory structure
        Use --final-dir to specify the new subdirectories for the files
    Stage 3: Let 'er rip.
        Use --git-remote, --git-branch, --save-shell-script, --save-shell-script-name
        --try-keep, and --execute to configuration execution
    """
    keepfiles = KeepFiles(file, directory, dir_structure == "FLAT")

    import pprint
    pprint.pprint(keepfiles.generate_commands())
    click.echo("!")

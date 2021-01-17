# git-repo-move

Move files from one git repo to another, preserving history!
Under the hood, this utility uses [`git filter-branch`](https://git-scm.com/docs/git-filter-branch), but the API is much more user friendly.

## How-To

### Install

```sh
pip install git-repo-move
```

### Build Locally

```sh
poetry build
```

### Run It

If you've already installed in via `pip`, it's really easy to use.
The program is called `git-repo-move`.
You can also checkout the source and build locally by running:

```sh
poetry install --no-dev
```

#### Select Files and Directories

Select what files you want to keep by specifying:

```sh
--file path/to/file.txt --file path/to/another_file.txt
```

and what directories you want to keep by specifying:

```sh
--directory path/to/subfolder --directory path/to_another subfolder
```

#### Select the Final Directory for the files

Optionally, specify the final directory for the files

```sh
--final_directory newpath/to/thefiles
```

#### Select Directory Structure

You can either flatten all files or keep the original directory structure

```sh
--directory-structure <FLAT|ORIGINAL>
```

For example:

```sh
--file path/to/file.txt --final-directory newpath/to/thefiles --directory-structure FLAT
```

`flat.txt` will end up at `newpath/to/thefiles/flat.txt`

```sh
--file path/to/file.txt --final-directory newpath/to/thefiles --directory-structure ORIGINAL
```

`flat.txt` will end up at `newpath/to/thefiles/path/to/file.txt

#### Specify the Git Remote URL of the Destination Repo

You can run `git remote -v` in the new repo to get a list of remote URLS.

```sh
--git-remote-url git@github.com:AlanRosenthal/git-repo-move.git
```

#### Specify the Git Branch Name

Remember this branch will used on both repos.

```sh
--git-branch move_files
```

#### Save Shell Script

This utility generates a shell script.
By default, the script will be saved in the root of the repo with the name `git-repo-move.sh`.

You can change the default name by specifying

```sh
--shell-script-name best-script-ever.sh
```

It's recommended to include the generate shell script on your PR.

Optionally, don't save a shell script by specifying the `--dont-save-shell-script` flag.


#### Try It Out

This utility uses `git-filter-branch` which is relatively slow, especially for large repos.
If also often takes a few attempts to specify the correct files and directories.

By specifying the `--try-it` flag, `git-repo-move` will move the files outside of git into a folder.
Inspect the files in that folder to ensure everything is correct.

#### execute

By specifying the `--execute` flag, the generated script will be executed.

### Example

We're using [`click`](https://github.com/pallets/click/) for the example.

We want to save [`src/click/formatting.py`](https://github.com/pallets/click/blame/2fc486c880eda9fdb746ed8baa49416acab9ea6d/src/click/formatting.py) and [`src/click/parser.py`](https://github.com/pallets/click/blame/2fc486c880eda9fdb746ed8baa49416acab9ea6d/src/click/parser.py) and have them end up in the folder `alan/click`.

Running the command:

```sh
git-repo-move --file click/formatting.py --file src/click/formatting.py --file click/parser.py --file src/click/parser.py --final_directory alan/click --directory-structure flat --git-remote-url git@github.com:AlanRosenthal/git-repo-move.git --git-branch move_files_example --execute
```

Note: We're including both `click/formatting.py` and `src/click/formatting.py` because `formatting.py` was moved from `click` to `src/click`.
`git-blame` knows how to capture files history across moves, but `git-filter-branch` does not.

As you can see, the [`move_files_example` branch](https://github.com/AlanRosenthal/git-repo-move/tree/move_files_example) has contains two files, `formatting.py` and `parser.py`.
Both files contain the history from their original repo.

from git_repo_move.keepfiles import KeepFiles

def test_single_file_flat():
    files = ["path/to/test1.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=True, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/test1.txt keep1234/the/final/countdown/test1.txt"
    ]

def test_multiple_files_flat():
    files = ["path/to/test1.txt", "path/to/test2.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=True, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/test1.txt keep1234/the/final/countdown/test1.txt",
        "mv -f path/to/test2.txt keep1234/the/final/countdown/test2.txt"
    ]

def test_single_file_not_flat():
    files = ["path/to/test1.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=False, final_directory="the/final/countdown")
    # print(keep_files.generate_commands())
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mkdir -p keep1234/the/final/countdown/path/to",
        "mv -f path/to/test1.txt keep1234/the/final/countdown/path/to/test1.txt"
    ]

def test_multiple_file_not_flat():
    files = ["path/to/folder1/test1.txt", "path/to/folder2/test2.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=False, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mkdir -p keep1234/the/final/countdown/path/to/folder1",
        "mkdir -p keep1234/the/final/countdown/path/to/folder2",
        "mv -f path/to/folder1/test1.txt keep1234/the/final/countdown/path/to/folder1/test1.txt",
        "mv -f path/to/folder2/test2.txt keep1234/the/final/countdown/path/to/folder2/test2.txt"
    ]

def test_single_dir_flat():
    dirs = ["path/to/test1"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=True, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/test1/* keep1234/the/final/countdown"
    ]

def test_multiple_dir_flat():
    dirs = ["path/to/test1", "path/to/test2"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=True, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/test1/* keep1234/the/final/countdown",
        "mv -f path/to/test2/* keep1234/the/final/countdown"
    ]

def test_single_dir_not_flat():
    dirs = ["path/to/test1"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=False, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/test1 keep1234/the/final/countdown"
    ]

def test_multiple_dir_not_flat():
    dirs = ["path/to/test1", "path/to/test2"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=False, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/test1 keep1234/the/final/countdown",
        "mv -f path/to/test2 keep1234/the/final/countdown"
    ]

def test_files_and_dir_flat():
    files = ["path/to/folder1/test1.txt", "path/to/folder2/test2.txt"]
    dirs = ["different/folder/test1", "another/folder/test2"]
    keep_files = KeepFiles(keep_files=files, keep_directories=dirs, is_dir_structure_flat=True, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mv -f path/to/folder1/test1.txt keep1234/the/final/countdown/test1.txt",
        "mv -f path/to/folder2/test2.txt keep1234/the/final/countdown/test2.txt",
        "mv -f different/folder/test1/* keep1234/the/final/countdown",
        "mv -f another/folder/test2/* keep1234/the/final/countdown"
    ]

def test_files_and_dir_not_flat():
    files = ["path/to/folder1/test1.txt", "path/to/folder2/test2.txt"]
    dirs = ["different/folder/test1", "another/folder/test2"]
    keep_files = KeepFiles(keep_files=files, keep_directories=dirs, is_dir_structure_flat=False, final_directory="the/final/countdown")
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234/the/final/countdown",
        "mkdir -p keep1234/the/final/countdown/path/to/folder1",
        "mkdir -p keep1234/the/final/countdown/path/to/folder2",
        "mv -f path/to/folder1/test1.txt keep1234/the/final/countdown/path/to/folder1/test1.txt",
        "mv -f path/to/folder2/test2.txt keep1234/the/final/countdown/path/to/folder2/test2.txt",
        "mv -f different/folder/test1 keep1234/the/final/countdown",
        "mv -f another/folder/test2 keep1234/the/final/countdown"
    ]


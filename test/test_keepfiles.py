from git_repo_move.keepfiles import KeepFiles

def test_single_file_flat():
    files = ["path/to/test1.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=True)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mv -f path/to/test1.txt keep1234/test1.txt"
    ]

def test_multiple_files_flat():
    files = ["path/to/test1.txt", "path/to/test2.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=True)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mv -f path/to/test1.txt keep1234/test1.txt",
        "mv -f path/to/test2.txt keep1234/test2.txt"
    ]

def test_single_file_not_flat():
    files = ["path/to/test1.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=False)
    # print(keep_files.generate_commands())
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mkdir -p keep1234/path/to",
        "mv -f path/to/test1.txt keep1234/path/to/test1.txt"
    ]

def test_multiple_file_not_flat():
    files = ["path/to/folder1/test1.txt", "path/to/folder2/test2.txt"]
    keep_files = KeepFiles(keep_files=files, keep_directories=(), is_dir_structure_flat=False)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mkdir -p keep1234/path/to/folder1",
        "mkdir -p keep1234/path/to/folder2",
        "mv -f path/to/folder1/test1.txt keep1234/path/to/folder1/test1.txt",
        "mv -f path/to/folder2/test2.txt keep1234/path/to/folder2/test2.txt"
    ]

def test_single_dir_flat():
    dirs = ["path/to/test1"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=True)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mv -f path/to/test1/* keep1234"
    ]

def test_multiple_dir_flat():
    dirs = ["path/to/test1", "path/to/test2"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=True)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mv -f path/to/test1/* keep1234",
        "mv -f path/to/test2/* keep1234"
    ]

def test_single_dir_not_flat():
    dirs = ["path/to/test1"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=False)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mv -f path/to/test1 keep1234"
    ]

def test_multiple_dir_not_flat():
    dirs = ["path/to/test1", "path/to/test2"]
    keep_files = KeepFiles(keep_files=(), keep_directories=dirs, is_dir_structure_flat=False)
    assert keep_files.generate_commands() == [
        "mkdir -p keep1234",
        "mv -f path/to/test1 keep1234",
        "mv -f path/to/test2 keep1234"
    ]


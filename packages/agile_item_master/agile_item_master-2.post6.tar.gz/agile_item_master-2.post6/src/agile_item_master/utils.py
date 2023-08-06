def ensure_directory_exists(path):
    from os.path import exists, isdir
    from os import makedirs
    if not exists(path):
        makedirs(path)
    assert isdir(path)
    return path

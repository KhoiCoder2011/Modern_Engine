import shutil

def copy_folder(src, dest):
    shutil.copytree(src, dest)
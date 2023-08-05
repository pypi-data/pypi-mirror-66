import os

def init_project_directory():
    os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
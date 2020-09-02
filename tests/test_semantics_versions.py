import os
from os.path import normpath, basename
import pytest
import simplejson as json

SEMANTICS_VERSION_PATH = os.path.join(".", "semantics_versions.json")
SEMANTICS_FOLDER_PATH = os.path.join(".", "semantics")

IGNORED_DIRS =['.DS_Store', '.git']

def get_semantics_versions():
    with open(SEMANTICS_VERSION_PATH, 'r') as semantics_versions_file:
        try:
            semantics_versions = json.load(semantics_versions_file)
            return semantics_versions
        except json.errors.JSONDecodeError:
            pytest.fail(f"Incorrect semantics_versions file.")


def test_semantics_folder_exist():
    assert os.path.exists(SEMANTICS_FOLDER_PATH), f"Semantics folder does not exists at {SEMANTICS_FOLDER_PATH}"


def test_semantics_versions_file_exists():
    assert os.path.exists(SEMANTICS_VERSION_PATH), f"Semantics versions file does not exists at {SEMANTICS_VERSION_PATH}"
    semantics_versions = get_semantics_versions()    
    assert semantics_versions is not None, f"Semantics versions file is empty"


def test_all_semantics_projects_are_defined_in_semantics_versions():
    semantics_versions = get_semantics_versions()    
    project_directories = [basename(normpath(f.path)) for f in os.scandir(SEMANTICS_FOLDER_PATH) if f.is_dir] 
    for project_directory in [ project_dir for project_dir in project_directories if project_dir not in IGNORED_DIRS]:
        assert project_directory in semantics_versions, f"Semantics project: {project_directory} is not defined in semantics versions file"


def test_all_defined_semantics_versions_have_corresponding_version_folder():
    semantics_versions = get_semantics_versions()
    for project_name, version in semantics_versions.items():
        project_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version)
        assert os.path.exists(project_path), f"Project {project_name} does not have version {version}"


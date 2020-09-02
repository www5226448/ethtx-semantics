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


def test_all_contract_semantics_have_abi_file():
  semantics_versions = get_semantics_versions()
  
  for project_name, version in semantics_versions.items():
    project_contracts_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version, "contracts")
    contracts_directories = [basename(normpath(f.path)) for f in os.scandir(project_contracts_path) if f.is_dir] 
    for contract in contracts_directories:
      abi_file_path = os.path.join(project_contracts_path, contract, "abi.json")
      abi_file_exists = os.path.exists(abi_file_path)
      assert abi_file_exists, f"No ABI file for project: {project_name} in version: {version} contract sementics: {contract}"
      with open(abi_file_path, 'r') as abi_file:
        try:
          json.load(abi_file)
        except json.errors.JSONDecodeError:
          pytest.fail(f"Incorrect ABI.json file for project: {project_name} in version: {version} contract sementics: {contract}")
          

def test_all_contract_semantics_with_transformations_are_correct():
  semantics_versions = get_semantics_versions()
  for project_name, version in semantics_versions.items():
    project_contracts_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version, "contracts")
    contracts_directories = [basename(normpath(f.path)) for f in os.scandir(project_contracts_path) if f.is_dir] 
    for contract in contracts_directories:
      transfromation_file_path = os.path.join(project_contracts_path, contract, "transformations.json")
      if os.path.exists(transfromation_file_path):
        with open(transfromation_file_path, 'r') as transformation_file:
          try:
            json.load(transformation_file)
          except json.errors.JSONDecodeError:
            pytest.fail(f"Incorrect Transformations.json file for project: {project_name} in version: {version} contract sementics: {contract}")
    

def test_all_contract_semantics_with_erc20_are_correct():
  semantics_versions = get_semantics_versions()
  for project_name, version in semantics_versions.items():
    project_contracts_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version, "contracts")
    contracts_directories = [basename(normpath(f.path)) for f in os.scandir(project_contracts_path) if f.is_dir] 
    for contract in contracts_directories:
      erc20_file_path = os.path.join(project_contracts_path, contract, "erc20.json")
      if os.path.exists(erc20_file_path):
        with open(erc20_file_path, 'r') as erc20_file:
          try:
            json.load(erc20_file)
          except json.errors.JSONDecodeError:
            pytest.fail(f"Incorrect ERC20.json file for project: {project_name} in version: {version} contract sementics: {contract}")
    

def test_all_contract_semantics_with_storage_are_correct():
  semantics_versions = get_semantics_versions()
  for project_name, version in semantics_versions.items():
    project_contracts_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version, "contracts")
    contracts_directories = [basename(normpath(f.path)) for f in os.scandir(project_contracts_path) if f.is_dir] 
    for contract in contracts_directories:
      storage_file_path = os.path.join(project_contracts_path, contract, "storage.json")
      if os.path.exists(storage_file_path):
        with open(storage_file_path, 'r') as storage_file:
          try:
            json.load(storage_file)
          except json.errors.JSONDecodeError:
            pytest.fail(f"Incorrect Storage.json file for project: {project_name} in version: {version} contract sementics: {contract}")
    

def test_all_contract_semantics_with_classification_are_correct():
  semantics_versions = get_semantics_versions()
  for project_name, version in semantics_versions.items():
    project_contracts_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version, "contracts")
    contracts_directories = [basename(normpath(f.path)) for f in os.scandir(project_contracts_path) if f.is_dir] 
    for contract in contracts_directories:
      classification_file_path = os.path.join(project_contracts_path, contract, "classification.json")
      if os.path.exists(classification_file_path):
        with open(classification_file_path, 'r') as classification_file:
          try:
            json.load(classification_file)
          except json.errors.JSONDecodeError:
            pytest.fail(f"Incorrect Classification.json file for project: {project_name} in version: {version} contract sementics: {contract}")
    
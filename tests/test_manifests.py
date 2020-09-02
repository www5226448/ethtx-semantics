import os
from os.path import normpath, basename
import pytest
import simplejson as json
import ruamel.yaml as rYaml
from web3 import Web3
import re
from collections import defaultdict

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


def get_project_manifest(project_name, version):
  project_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version)
  with open(os.path.join(project_path, 'manifest.yaml'), 'r') as manifest_file:
    yaml = rYaml.YAML(typ='safe')
    project_manifest = yaml.load(manifest_file)
    assert project_manifest, f"Manifest for project {project_name} in version {version} is empty"
    return project_manifest


def check_addresses_metadata(network, addresses_metadata, project_name, version, contract_semantics):
  network_metadata = addresses_metadata.get(network, None)
  assert network_metadata is not None, f'No mainnet metadata for contract {contract_semantics} in manifest file for project {project_name} in version {version}'
  for address, addresses_metadata in network_metadata.items():
    assert Web3.isAddress(address), f'Address {address} is wrong in {network} for contract {contract_semantics} in manifest file for project {project_name} in version {version}'
    assert "label" in addresses_metadata, f'No label for address {address} for network {network}'


def check_code_hashes_metadata(applicable_to_contracts_with_code_hash, project_name, version, contract_semantics):
  for code_hash in applicable_to_contracts_with_code_hash:
    is_correct_code_hash = re.search('0[xX][0-9a-fA-F]{64}', code_hash)
    assert is_correct_code_hash, f'Code hash {code_hash} is incorrect in manifest in contract {contract_semantics} for project {project_name} in version {version}'


def test_all_projects_have_correct_manifests():
  semantics_versions = get_semantics_versions()

  for project_name, version in semantics_versions.items():
    manifest = get_project_manifest(project_name, version)
    
    for contract_semantics, metadata in manifest.items():
      contract_semantics_path = os.path.join(SEMANTICS_FOLDER_PATH, project_name, version, "contracts", contract_semantics)

      semantics_folder_exists = os.path.exists(contract_semantics_path)
      assert semantics_folder_exists, f'Contract semantics folder {contract_semantics} does not exist for project {project_name} in version {version}'

      addresses_metadata = metadata.get('addresses', None)
      assert addresses_metadata is not None, f'No addresses metadata for contract {contract_semantics} in manifest file for project {project_name} in version {version}'

      undefined_network_metadata = addresses_metadata.get("*", None)
      assert undefined_network_metadata is not None, f'No * network metadata for contract {contract_semantics} in manifest file for project {project_name} in version {version}'
      # assert "label" in undefined_network_metadata, f"No label in * network metadata for contract {contract_semantics} in manifest file for project {project_name} in version {version}"

      check_addresses_metadata("mainnet", addresses_metadata, project_name, version, contract_semantics)
      check_addresses_metadata("kovan", addresses_metadata, project_name, version, contract_semantics)
      check_addresses_metadata("ropsten", addresses_metadata, project_name, version, contract_semantics)

      code_hashes_metadata = metadata.get('applicable_to_contracts_with_code_hash', None)
      assert code_hashes_metadata is not None, f'No applicable_to_contracts_with_code_hash metadata for contract {contract_semantics} in manifest file for project {project_name} in version {version}'

      check_code_hashes_metadata(code_hashes_metadata, project_name, version, contract_semantics)


def test_every_code_hash_is_defined_only_once():
  semantics_versions = get_semantics_versions()
  code_hash_to_semantics_mapping = defaultdict(lambda: [])

  for project_name, version in semantics_versions.items():
    manifest = get_project_manifest(project_name, version)
    for contract_semantics, metadata in manifest.items():
      code_hashes_defined_for_contract = metadata.get('applicable_to_contracts_with_code_hash', None)
      for code_hash in code_hashes_defined_for_contract:
        semantics_key = (project_name, version, contract_semantics)
        code_hash_to_semantics_mapping[code_hash].append(semantics_key)
  
  for code_hash, semantics_list in code_hash_to_semantics_mapping.items():
    assert len(semantics_list) == 1, f'Code hash {code_hash} defined for multiple contracts {semantics_list}'

def test_every_address_is_defined_only_once_for_network():
  semantics_versions = get_semantics_versions()

  addresses_per_network_mapping = defaultdict(lambda: {})

  for project_name, version in semantics_versions.items():
    manifest = get_project_manifest(project_name, version)
  
    for contract_semantics, metadata in manifest.items():
      addresses_metadata = metadata.get('addresses', {})
      for network, addresses in addresses_metadata.items():
        semantics_key = (project_name, version, contract_semantics)
        for address in addresses:
          if address in addresses_per_network_mapping[network]:
            addresses_per_network_mapping[network][address].append(semantics_key)
          else:
            addresses_per_network_mapping[network][address] = [semantics_key]

  for network, addresses in addresses_per_network_mapping.items():
    for address, semantics_keys in addresses.items():
      assert len(semantics_keys) == 1, f"Address {address} defined multiple timest for {network} in {semantics_keys}"
def number_of_decimals(know_addresses_registry, _transaction, contract_address, default=18):
    if contract_address is not None:
        known_address, contract, address_info = know_addresses_registry.register(contract_address)
        if address_info and address_info['coin'] and address_info['coin']['dec']:
            return address_info['coin']['dec']

    return default
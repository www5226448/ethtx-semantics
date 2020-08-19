# EthTx - community semantics

The purpose of this project is to provide smart contract descriptions for the EthTx decoder.

Check [Community EthTx.info](https://community.ethtx.info/) for the live version. Code base is stored [here](https://github.com/makerdao/ethtx)

## EthTx decoder

Ethtx is an advanced decoder for Ethereum transactions. Ethtx translates unreadable transaction data into an easy understandable language through its semantic system. This semantic system gives users ability to add their contract ABIs and add rich context for each function data in the contracts so as to allow an easy read of transactions.

When interacting with more than a simple smart contract on the Ethereum network it becomes quite impossible to figure out the nitty details of the transaction that you performed. You can see that you send some amount of tokens to a smart contract and received some in return, but you can't easily figure out what exact function calls have been performed in each contract during the transaction.

On etherscan, besides seeing the movement of your tokens you're presented with, you can see the encoded transaction details like this:

```jsx
Function: execute(address _wallet, bytes _data, uint256 _nonce, bytes _signatures, uint256 _gasPrice, uint256 _gasLimit)

MethodID: 0xaacaaf88
[0]:  000000000000000000000000233ae6edc762336b177af882960dee989276b2cc
[1]:  00000000000000000000000000000000000000000000000000000000000000c0
[2]:  0000000000000000000000000099a9060000000000000000000000005ebe735e
[3]:  0000000000000000000000000000000000000000000000000000000000000180
...
```

Now with Ethtx decoder, you can contextually see each step taken through each contract. See this transaction as an example.

![Alt Text](https://i.imgur.com/5IqFMfO.gif)

Supported networks:

- mainnet
- kovan
- ropsten

## Contract Semantics

This repository contains directories defined per project. The project is grouping of the smart contracts semantics usually by their deployer like `makerdao`, `oasis` or `dydx`. Every project can have multiple versions of semantics. They are stored in separated folders named after the version - for example `makerdao` project has two versions: `1.0.8` and `1.0.9`. We encourage to use the semantic versioning for as a naming convention.

The currently used version of the contract semantics should be defined in the `semantics_versions.json` file to be used by the EthTx decoder.

**Versioned semantics folder** has the following structure:

- **contracts** directory - it contains named smart contracts semantics - for example `MCD_Vat` (name is only used to match deployed contract address with semantics). Each semantics folder can contain the following files:

  - `abi.json` - [ABI](https://solidity.readthedocs.io/en/v0.5.3/abi-spec.html#json) file of the smart contract.
  - **[ Optional ]** `transformations.json` - file with the description how functions and events arguments should be transformed by the decoder. Structure of this file is described [here](#semantics-file-descriptions).
  - **[ Optional ]** `storage.json` - file with the description of the contract storage based on how the compiler creates the storage layout. Structure of this file is described [here](#semantics-file-descriptions).
  - **[ Optional ]** `erc20.json` - file with the basic information of the EC20 token. Contains token name, symbol and number of decimals. This information can be overridden by the metadata from the `manifest.yaml` file. Structure of this file is described [here](#semantics-file-descriptions).

- **functions** optional directory - which should contain a file `__init__.py` where all functions used by smart contracts semantics are defined. Other files and subdirectories in this folder are up to the semantics creator. Functions defined here can be used in every `transformations.json` file for this semantics version.

- **manifest.yaml** file - this file represents mapping of smart contracts semantics to deployed addresses. It adds also a metadata for every address. Structure of this file is described [here](#manifest-file-description).

## Manifest file description

The purpose of the `manifest.yaml` file is to define which addresses should be decoded using the smart contract sematics defined in the `contracts` directory. Basic structure looks like this:

```yaml
MCD_DAI:
  addresses:
    "*":
      label: MCD_DAI
    mainnet:
      "0x6B175474E89094C44Da98b954EedeAC495271d0F":
        label: DAI
        erc20:
          name: "Dai Stablecoin"
          symbol: "DAI"
          dec: 18
    ropsten: {}
    kovan:
      "0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa":
        label: Kovan_DAI
        erc20:
          name: "Dai Stablecoin"
          symbol: "DAI"
          dec: 18

  applicable_to_contracts_with_code_hash:
    - "0x4e36f96ee1667a663dfaac57c4d185a0e369a3a217e0079d49620f34f85d1ac7"
```

The name of the structure is name of the smart contract semantics - in this example `MCD_DAI`. It is required that there is a subdirectory named `MCD_DAI` in the `contracts` directory.

The top parameters of the semantics metadata are:

- `addresses:` - in this section we define metadata of known addresses deployed to supported networks.

  - `"*"` section defines metadata applied to every address not defined in latter sections. Right now only the `label` is supported here. To define ERC20 token metadata use `erc20.json` file in the semantics directory.
  - `mainnet`, `kovan` and `ropsten` sections define addresses metadata for those deployed on those network.
    If the EthTx decoder encounters on of the addresses defined here it will apply the semantics to it.
    You can define a `label` under which this address should be visible in the EthTx decoder output and `erc20` metadata is this address is an ERC20 token and you want to override the data stored in the `erc20.json` in the semantics directory.

- `applicable_to_contracts_with_code_hash` - it is an array of contract code hashes that this semantics can be used for. When the EthTx decoder encounters a deployed contract that has an EVM bytecode that can be hashed to one of those values it will automatically apply the semantics during decoding. Those hashes can be reused if deploying same contract on other Ethereum networks.

## Semantics file descriptions

### `transformations.json`

The transformations file allows creating an additional layer of processing on top of the ABI of the contract. This processing can be done to each function or event that the contract contains. These functions or events have a signature hash that can be found in the `abi.json` file.

Looking at an the event in the `DsrExample` contract interface:

```jsx
event DaiBalance(address indexed src, uint balance);
```

We can see that it has two arguments, `address` and `balance`. Balance is an `uint` type. In the EthTx explorer, this number is represented in `wei` format, i.e. a number with 18 decimal places. Like this: `1000000000000000000`. With the Format semantic tool, we can add a processing function for this number type that can be converted to human readable format.

In the ABI window, you can find the signature hash of every event or function available in the contract.

By using the event `DaiBalance` signature hash, for example: `0x5139b2b06a1d8192b7f9a6232286a17737fe00a2d0c7efc217f863759d870007`, you can start formatting the parameters of this function.

In the `transformation.json` file, you can switch the editor to `code` and write in `JSON` format the processing function. Below is an example:

```json
{
  "0x5139b2b06a1d8192b7f9a6232286a17737fe00a2d0c7efc217f863759d870007": {
    "arguments": {
      "balance": {
        "path": "balance",
        "type": "uint256",
        "value": " balance / 10**18"
      }
    }
  }
}
```

In this example, the `event DaiBalance` signature hash has been taken and used as the reference to modify its `balance` argument to our desired goal. We want to display `balance` in a decimal point number. As it can be observed in the above example, we structure the JSON object to modify the specific `balance` argument of the `DaiBalance` event. The actual conversion is happening at the `value` key, where its value is `balance / 10**18`. EthTx takes `python3` functions that can be processed in the backend to format types to your desired state. `Python3` functions can be defined as one line function in the `transformations.json` file `"value": " balance / 10**18"` or use a function defined in the `functions/__init__.py` file of the semantics project.

### `storage.json`

The `storage.json` file allows decoding the internal storage of a contract. Before starting to decode each variable in the contract, you'll have to know exactly where each variable is stored inside the memory of the contract. In other words, which `slot` holds which variable. To learn more about how variables are stored in the contract, have a read at the [Solidity Layout of State Variables in Storage documentation.](https://solidity.readthedocs.io/en/v0.6.10/internals/layout_in_storage.html)

As a basic rule, to identify the position of variables in the contract, you start at the beginning of where the first variable is being declared.
For example, looking at the Vat contract:

```js
contract Vat {
    // --- Auth ---
    mapping (address => uint) public wards;
    function rely(address usr) external note auth { require(live == 1, "Vat/not-live"); wards[usr] = 1; }
    function deny(address usr) external note auth { require(live == 1, "Vat/not-live"); wards[usr] = 0; }
    modifier auth {
        require(wards[msg.sender] == 1, "Vat/not-authorized");
        _;
    }

    mapping(address => mapping (address => uint)) public can;
    function hope(address usr) external note { can[msg.sender][usr] = 1; }
    function nope(address usr) external note { can[msg.sender][usr] = 0; }
    function wish(address bit, address usr) internal view returns (bool) {
        return either(bit == usr, can[bit][usr] == 1);
    }
```

The first variable being stored in the contract is `wards`. This means that `wards` has the `slot` position equal to zero: `slot=0`. The `can` variable is in position `slot=1`, etc.

To decode the `wards` variable look at the example below:

```json
[
  {
    "end": 63,
    "hashmap": {
      "key1": "address",
      "key2": null,
      "struct": null,
      "value": "int"
    },
    "name": "wards",
    "slot": 0,
    "start": 0,
    "type": "hashmap"
  }
]
```

**NOTE:** Solidity can store more than one variable in the same slot in the contract storage if it deems it small enough to fit. So, sometimes you might find that let's say in `slot=0` there can be more than one variable. Each slot has 64 bytes storage. So, one variable can be stored from position 0 to 8 and the other from position 9 to 63 in the same slot.

To understand how many other variables are decoded, let's look at the full [MCD_VAT contract variable decodings](makerdao/1.0.9/contracts/MCD_VAT/storage.json).

Looking at our DsrExample contract, we see that we only have one variable: `owner`:

```js
contract DsrExample {

    // Contract Interfaces
    DsrManager public dsrM;
    GemLike  public daiToken;

    address owner;

    event DaiBalance(address indexed src, uint balance);
}
```

Adding semantics for this variable in the storage window should look like this:

```json
[
  {
    "end": 63,
    "hashmap": null,
    "name": "owner",
    "slot": "0",
    "start": "0",
    "type": "address"
  }
]
```

### `erc20.json`

The `erc20.json` file allows to store basic ERC20 token metadata: `name`, `symbol` and `dec` - the number of decimal places. Here is an example of this file for the `WETH` token:

```json
{
  "symbol": "WETH",
  "name": "Wrapped Ether",
  "dec": 18
}
```

**NOTE** All data provided here can be overridden by the metadata from the `manifest.yaml` file if `erc20` section of address is defined.

## Semantics functions module

If you need a more complex transformation for the smart contract semantics in the `transformation.json` you can define them in the `functions` directory which is a Python module with `__init__.py` file. This file should contain imports or definition of all functions that are used in the following version of the semantics:

Here is an example of function that can be used in the `transformation.json` file:

```python
def number_of_decimals(know_addresses_registry, _transaction, contract_address, default=18):
    if contract_address is not None:
        known_address, contract, address_metadata = know_addresses_registry.register(contract_address)
        if address_metadata and address_metadata['coin'] and address_metadata['coin']['dec']:
            return address_metadata['coin']['dec']

    return default
```

The name of the function should be meaningful but there are no restrictions how it should be named.
The first and second parameters are required to be `know_addresses_registry` and `transaction`. The following parameters are optional and to be defined by the function creator.

The function can be later used in the `transformation.json` ih the following manner:

```json
"srcAmount": {
  "path": "srcAmount",
  "type": "uint256",
  "value": "srcAmount / 10 ** number_of_decimals(src, default=18)"
}
```

**NOTE**: You never add the first two function arguments (`known_address_registry` and `transaction`) they are always injected for you by the EthTx decoder. They can be used for more advanced transformations and you can ignore them if you won't use them.

The first argument is the `known_address_registry` which exposes the `register(address)` method which returns a tuple with 3 elements:

- `known_address` - object with basic information of the address. Has the following properties: `address`, `network`, `etherscan_url`, `label`

- `contract_semantics` - dictionary with the contract semantics available for the given address. The main keys in this dictionary are `formats` (contains the information stored in `transactions.json` file), `storage` (contains the information stored in `storage.json` file), `erc20` (contains the information stored in `erc20.json` file)

- `address_metadata` - dictionary with the address metadata taken from the `manifest.yaml` file. It contains the `network`, `address`, `label` and `coin` keys. Under the `coin` key is a dictionary with the data defined in the `erc20.json` file or `erc20:` section of the given address metadata defined in the `manifest.yaml` file.

The second argument is the `transaction` which is a dictionary with the following keys:

- `hash` - transaction hash

- `blockNumber`

- `gas_price`, `gas_used`, `cost` - contain information about gas used by the transaction.

- `from` - the address of transaction sender

- `to` - the address of transaction receiver

- `contractAddress` - the address of receiving contract taken from the transaction receipt

- `value` - string representation of the sent ether `value`

- `logs` - the array of logs created by the transaction. Represented as dictionary with keys `address`, `topics` and `data`

## Versioning of semantics

The EthTx decoder by default uses versions of the semantics defined in the `semantics_versions.json` file. The file structure looks like this:

```json
{
  "makerdao": "1.0.9",
  "oasis": "0.0.1",
  "wrapped-ether": "0.0.1"
}
```

In this example the decoder will look for semantics defined in folders `makerdao/1.0.9`, `oasis/0.0.1` and `wrapped-ether/0.0.1`.

If you deploy your own instance of the EthTx decoder you can pin the version of the used semantics in the `required_semantics.json` file in the top directory of the EthTx codebase. For example, if the `required_semantics.json` looks like this:

```json
{
  "makerdao": "1.0.8"
}
```

then the deployed EthTx decoder will use `makerdao/1.0.8` semantics _and_ all other semantics defined int the `semantics_versions.json` file.

# How to create a new semantics project?

1. Create a new folder with a chosen project name. For example: `cube`.

2. In it create a new directory with the project version. For example: `0.0.1`.

3. Create a `contracts` subdirectory in the main folder.

4. Create a `manifest.yaml` file.

5. In the `manifest.yaml` file create a section with the name of the semantics. Make sure that the name of the semantics can be a directory name. For example: `CubeTimer`. The structure of this file is defined in the README.

```yaml
CubeTimer:
  addresses:
    "*":
      label: Timer
    mainnet:
      "0x3cc067f4d6ef35a540c1d0ec933477b915fcc169":
        label: MainnetTimer
    kovan:
      "0x3cc067f4d6ef35a540c1d0ec933477b915fcc228":
        label: KovanTimer
    ropseten: {}
  applicable_to_contracts_with_code_hash:
    - "0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
```

6. In the `contracts` create a subdirectory named the same as the section in the `manifest.yaml` file. In our example it's `CubeTimer`

7. In the semantics folder create a `abi.json` file with the ABI of the defined smart contract.

8. In the semantics folder you can create optional files. All the files are described in the README.

- `transformations.json` if you wish to transform defined smart contract events arguments or inputs and outputs of its functions.
- `storage.json` if you with to describe storage of your contract and have `State diffs` available for your contract in the EthTx decoder output.
- `erc20.json` - if your semantics describe an ERC20 compatible smart contract, you can put the basic information of the token here: its name, symbol and number of decimals.

9. If during the development process you encounter a more complex transformation you can create a Python module with needed functions. Create a folder named `functions` at the same level as `contracts` and `manifest.yaml`. You are required to have a file **init**.py that contains all the python functions for use in the `transformations.json` file.

10. In the end the project directory should have the following structure:

```text
cube
  - 0.0.1
    - contracts
       - CubeTimer
       - CubeToken

    - functions
      - __init__.py

    - manifest.yaml
```

11. In the top directory of the repository is a file named `semantics_versions.json`. Add your project with the correct version to it. In the example it should look like this:

```json
{
  ...
  "cube" : "0.0.1",
  ...
}
```

12. Create a pull request with your semantics changes. Be patient and respond to any questions during the code review.

# How to create a new version of the existing semantics?

1. Copy the directory with the previous version of the semantics and name it with a higher number according to the [semantics versioning](https://semver.org/). For example: you copy the `1.0.8` version of the semantics and you will add minor changes as a directory `1.0.9`.

2. Apply your changes. Edit existing semantics, add a new semantics, add addresses to the existing semantics, introduce a new functions available for transformations.

3. Bump the version of the semantics in the `semantics_versions.json` in the directory of the repository.

4. Create a Pull Request with your changes. Be patient and respond to any questions during the code review.

# Can I edit exiting version of the semantics?

Yes, as long as add new addresses for the exiting semantics or add new version of optional semantics files.

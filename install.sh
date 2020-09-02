if ! command -v pipenv &> /dev/null
then
  echo "Pipenv command not found. Please install is using this guide:"
  echo "https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv"
  exit
fi

pipenv shell
pipenv install 
# This script should be sourced before using this repo (for development).
# It creates the python virtualenv and using pip to populate it
# This only run to setup the development environment.
# Installation is handled by setup.py/disttools.

# New python requirements should be added to pip-requires.txt
# This requires pip and virtualenv to be installed in the system path.

if [ -d ".venv" ]; then
   # Virtual Env exists
   true
else
   echo "**> creatinv virtualenv"
   virtualenv .venv --prompt "(katipo) " --extra-search-dir=$PWD
   # During development - add this folder to the PYTHONPATH
   echo -e "\n# Adding development pythonpath\nexport PYTHONPATH=\"$PWD:\$PYTHONPATH\"\n" >> $PWD/.venv/bin/activate
fi

source .venv/bin/activate
# readline must be come before everything else
# only need on Mac
if [[ `uname` == 'Darwin' ]]; then
   easy_install -i http://pypi.braincorporation.net/simple readline==6.2.2   
fi
pip install -q -r requirements.txt -i http://pypi.braincorporation.net/simple
pip install -q -r dev-requirements.txt -i http://pypi.braincorporation.net/simple

# Setup the PATH to point to packages (only needed for debugging - installion will use setuptools).
PATH=$PWD:$PATH


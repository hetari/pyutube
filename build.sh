# remove the previous build files
rm -rf dist

# Uninstall the package 'pyutube' — run this inside a virtualenv
pip uninstall pyutube -y

# Build a wheel distribution package using the 'setup.py' file
python3 setup.py sdist bdist_wheel

# Install the wheel distribution package located in the 'dist' directory
# pip3 install dist/*

# remove any random folder in all levels
find . -name '__pycache__' -exec rm -rf {} +
rm -rf pyutube.egg-info
rm -rf build
rm -rf pytest_cache

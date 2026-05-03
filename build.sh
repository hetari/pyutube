# remove the previous build files
rm -rf dist

# Uninstall the package 'pyutube' with the '-y' flag to confirm the uninstallation without user prompt
pip uninstall pyutube -y --break-system-packages

# Build a wheel distribution package using the 'setup.py' file
python3 setup.py sdist bdist_wheel

# Install the wheel distribution package located in the 'dist' directory
# pip3 install dist/*

# remove any random folder in all levels
find . -name '__pycache__' -exec rm -rf {} +
rm -rf pyutube.egg-info
rm -rf build
rm -rf pytest_cache

#!/bin/zsh
echo "Creating new environment using $(which python)"
python -m venv build_venv
source build_venv/bin/activate
echo "Using $(which python)"
pip install --upgrade build
python -m build
pip install --upgrade twine
echo "Use the build_venv: 'source build_venv/bin/activate'"
echo "Then upload using:  'python -m twine upload dist/*'"
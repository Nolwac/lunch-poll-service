@echo off
python -m pip install virtualenvwrapper==4.8.4 && mkvirtualenv %1 && workon %1 && python scripts/dev_environment_setup.py
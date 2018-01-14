@echo off
REM change to project root
cd %~dp0\..
REM delete old env quietly
rmdir /s /q env >nul 2>&1
REM make new virtual environment
python -m venv env
REM activate it
CALL env\Scripts\activate.bat
REM upgrade pip, install wheel
pip install --upgrade pip wheel
REM install dependencies
pip install -r requirements.txt
REM wait for user to close window
pause
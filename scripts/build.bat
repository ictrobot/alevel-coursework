@echo off
REM change to project root
cd %~dp0\..
REM clean build directory quietly
rmdir /s /q build 2> nul
REM activate python virtual environment
CALL env\Scripts\activate.bat
REM change to src dir
cd src
REM build exe
pyinstaller main.py -F -w --workpath ..\build\ --distpath ..\build\ --add-data ngram_data\*GRAM.txt;ngram_data\
REM delete main.spec
del main.spec 2> nul
REM wait for user to close window
pause
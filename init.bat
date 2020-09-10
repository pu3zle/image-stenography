@echo off 

goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system.
echo Please rerun this after installing Python
echo Now opening the download URL.
start "" "https://www.python.org/downloads/"
goto :EOF

:PYTHON_DOES_EXIST
:: This will retrieve Python 3.8.0 for example.
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo Congrats, %ver% is installed...
echo Initialising environment...
pip install -r requirements.txt
steno.py init
goto :EOF
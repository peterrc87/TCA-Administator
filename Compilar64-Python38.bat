@CLS
@ECHO OFF
ECHO Compilando...
set PATH=%PATH%;C:\Windows\System32\downlevel
py -3.8-64 setup.py build
pause
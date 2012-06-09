rem Put your data file under directory "data"
rem e.g. of usage
rem run.cmd comments.dat
rem run.cmd music.dat

%echo off
cd /d %0\..
cd ..
set PYTHONPATH="%PYTHONPATH%;%CD%\src;%CD%\src\main"
python -m main.Main %*

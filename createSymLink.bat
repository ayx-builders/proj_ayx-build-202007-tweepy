Pushd "%~dp0"
set destination=C:\ProgramData\Alteryx\Tools
mklink /D %destination%\tweepyx %CD%\

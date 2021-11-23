@echo off
if [%1]==[] goto blank

rmdir /s /q releases
cd frontend 
call yarn build
call yarn deploy && cd ..
if not exist "releases" (
    mkdir "releases"
)
xcopy backend\* releases\ /E /Y
copy requirements.txt releases\
cd releases 
for /d /r %%i in (*__pycache__*) do rmdir /s /Q "%%i"
rmdir /s /q cache
rmdir /s /q temp
for /d /r %%i in (*.env*) do rmdir /s /Q "%%i"
del GoogleSheets.ipynb
copy ..\.env_template .\api\.env
tar.exe -a -c -f "..\%1.zip" *
cd ..
goto exit 
:blank
Echo You have to pass the name of version
:exit
echo OK
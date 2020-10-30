:Begin
@echo off
color 1f
cls
ECHO. 
ECHO                  Profile Copier - Created by Kion Kaimi 2015
ECHO              Copy profile(s) from Win 7/XP to New Win 7 Machine
ECHO                    ::::: MAKE SURE TO RUN AS ADMIN :::::
ECHO.
ECHO ===============================================================================
ECHO.

cd /d C:\

:OldPC

set /p old_pc=Enter OLD Machine Name: 

if %old_pc%=="restart" goto Begin

if not exist \\%old_pc%\c$ ECHO Old PC Not Found.

if not exist \\%old_pc%\c$ goto OldPC

:NewPC

set /p new_pc=Enter NEW Machine Name: 

if %new_pc%=="restart" goto Begin

if not exist \\%new_pc%\c$ ECHO New PC Not Found.

if not exist \\%new_pc%\c$ goto NewPC

saveInfo.py "%old_pc%" "%new_pc%"

:start

ECHO.
ECHO Logged on user: 
ECHO.
wmic /node:"%old_pc%" computersystem get username
ECHO.
ECHO Printers on OLD machine:
ECHO.
wmic /node:"%old_pc%" printer get name, portname
ECHO.
ECHO Users on OLD machine:
ECHO.
DIR /O:-D /T:A /B "\\%old_pc%\c$\Users\"
ECHO.

set /p username=Enter Username: 
if %username%=="restart" goto Begin

for /f "delims= " %%a in ('"wmic path win32_useraccount where name='%username%' get sid"') do (
   if not "%%a"=="SID" (          
      set myvar=%%a
      goto :loop_end
   )   
)

:loop_end

REM if exist "https://protect-us.mimecast.com/s/pfqYCwp5G6HjvL63hq1G-h?domain=\\cs.msds.kp.org\scal\rvs\share27\itfs\_refresh\refresh Pairing\ProfileCopier.csv" pushd "https://protect-us.mimecast.com/s/pfqYCwp5G6HjvL63hq1G-h?domain=\\cs.msds.kp.org\scal\rvs\share27\itfs\_refresh\refresh Pairing"

REM ECHO %old_pc%,%new_pc%,%username%,%date%,%time% >> ProfileCopier.csv

cd /d C:\

mkdir "\\%new_pc%\c$\source\profile\%username%"

mkdir "\\%new_pc%\c$\source\profile\%username%\desktop"

mkdir "\\%new_pc%\c$\source\profile\%username%\Documents"

mkdir "\\%new_pc%\c$\source\profile\%username%\Pictures"

:Win7

ECHO Copying, please wait...

XCOPY /E /C /R /I /K /Y /Q "C:\source\citrixSwap" "\\%new_pc%\c$\source\citrixSwap"

XCOPY /E /C /R /I /K /Y /Q "\\%old_pc%\c$\Users\%username%\Desktop" "\\%new_pc%\c$\source\profile\%username%\desktop"

XCOPY /E /C /R /I /K /Y /Q "\\%old_pc%\c$\Users\%username%\Favorites" "\\%new_pc%\c$\source\profile\%username%\favorites"

XCOPY /E /C /R /I /K /Y /Q "\\%old_pc%\c$\Users\%username%\Documents" "\\%new_pc%\c$\source\profile\%username%\Documents"

echo F|XCOPY /E /C /R /I /K /Y /Q "\\%old_pc%\c$\Users\%username%\AppData\Local\Google\Chrome\User Data\Default\Bookmarks" "\\%new_pc%\c$\source\profile\%username%"

XCOPY /E /C /R /I /K /Y /Q "\\%old_pc%\c$\Users\%username%\AppData\Roaming\Microsoft\Signatures" "\\%new_pc%\c$\source\profile\%username%\Signatures"

XCOPY /E /C /R /I /K /Y /Q "\\%old_pc%\c$\Users\%username%\Pictures" "\\%new_pc%\c$\source\profile\%username%\Pictures"

if exist "\\%new_pc%\C$\source\profile\%username%\Network.reg" del "\\%new_pc%\C$\source\profile\%username%\Network.reg"

if exist "\\%new_pc%\C$\source\profile\%username%\Printers.reg" del "\\%new_pc%\C$\source\profile\%username%\Printers.reg"

REM wmic /node:%old_pc% process call create "reg export \"HKEY_USERS\%myvar%\Network" "\\%new_pc%\c$\source\profile\%username%\Network.reg" /y

REM wmic /node:%old_pc% process call create "reg export \"HKEY_USERS\%myvar%\Printers\Connections\" "\\%new_pc%\c$\source\profile\%username%\Printers.reg" /y

goto Output

:Output

pushd \\%new_pc%\c$\

md Temp

pushd \\%new_pc%\c$\Source\

md Profile
pushd "\\%new_pc%\c$\Source\Profile"
ECHO CD C:\ > %username%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%username%\Desktop" "C:\Users\%username%\Desktop" >> %username%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%username%\Favorites" "C:\Users\%username%\Favorites" >> %username%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%username%\Documents" "C:\Users\%username%\Documents" >> %username%.bat
ECHO echo F|XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%username%\Bookmarks" "C:\Users\%username%\AppData\Local\Google\Chrome\User Data\Default" >> %username%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%username%\Signatures" "C:\Users\%username%\AppData\Roaming\Microsoft\Signatures" >> %username%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%username%\Pictures" "C:\Users\%username%\Pictures" >> %username%.bat
ECHO taskkill /f /IM explorer.exe >> %username%.bat
ECHO start explorer.exe >> %username%.bat
ECHO start /b ^"^" cmd /c del ^"%%~f0^"^&exit /b >> %username%.bat

pushd "\\%new_pc%\c$\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"

ECHO @ECHO off > %username%.bat
ECHO if not exist C:\Users\%username% exit >> %username%.bat
ECHO if not exist "C:\source\profile\%username%.bat" exit >> %username%.bat
ECHO cd /d C:\ >> %username%.bat
ECHO ECHO Copying, please wait... >> %username%.bat
ECHO if exist "C:\source\profile\%username%\Network.reg" regedit /S "C:\source\profile\%username%\Network.reg" >> %username%.bat
ECHO if exist "C:\source\profile\%username%\Printers.reg" regedit /S "C:\source\profile\%username%\Printers.reg" >> %username%.bat
ECHO if exist "C:\source\profile\%username%.bat" "C:\source\profile\%username%.bat" >> %username%.bat
REM ECHO DEL /F/Q/S "C:\Source\Profile\%username%\desktop.ini" >> %username%.bat
ECHO ECHO. >> %username%.bat
ECHO ECHO Migration Complete >> %username%.bat
ECHO ECHO. >> %username%.bat
ECHO exit >> %username%.bat

net use * /d /y

goto start
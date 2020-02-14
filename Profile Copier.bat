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

set /p t=Enter OLD Machine Name: 

if %t%=="restart" goto Begin

if not exist \\%t%\c$ ECHO Old PC Not Found.

if not exist \\%t%\c$ goto OldPC

:NewPC

set /p z=Enter NEW Machine Name: 

if %z%=="restart" goto Begin

if not exist \\%z%\c$ ECHO New PC Not Found.

if not exist \\%z%\c$ goto NewPC

saveInfo.py %t% %z%

:start

ECHO.
ECHO Logged on user: 
ECHO.
wmic /node:%t% computersystem get username
ECHO.
ECHO Printers on OLD machine:
ECHO.
wmic /node:%t% printer get name, portname
ECHO.
ECHO Users on OLD machine:
ECHO.
DIR /O:-D /T:A /B "\\%t%\c$\Users\"
ECHO.

set /p r=Enter Username: 
if %r%=="restart" goto Begin

for /f "delims= " %%a in ('"wmic path win32_useraccount where name='%r%' get sid"') do (
   if not "%%a"=="SID" (          
      set myvar=%%a
      goto :loop_end
   )   
)

:loop_end

REM if exist "https://protect-us.mimecast.com/s/pfqYCwp5G6HjvL63hq1G-h?domain=\\cs.msds.kp.org\scal\rvs\share27\itfs\_refresh\refresh Pairing\ProfileCopier.csv" pushd "https://protect-us.mimecast.com/s/pfqYCwp5G6HjvL63hq1G-h?domain=\\cs.msds.kp.org\scal\rvs\share27\itfs\_refresh\refresh Pairing"

REM ECHO %t%,%z%,%r%,%date%,%time% >> ProfileCopier.csv

cd /d C:\

mkdir "\\%z%\c$\source\profile\%r%"

mkdir "\\%z%\c$\source\profile\%r%\desktop"

mkdir "\\%z%\c$\source\profile\%r%\Documents"

mkdir "\\%z%\c$\source\profile\%r%\Pictures"

:Win7

ECHO Copying, please wait...

XCOPY /E /C /R /I /K /Y /Q "C:\source\citrixSwap" "\\%z%\c$\source\citrixSwap"

XCOPY /E /C /R /I /K /Y /Q "\\%t%\c$\Users\%r%\Desktop" "\\%z%\c$\source\profile\%r%\desktop"

XCOPY /E /C /R /I /K /Y /Q "\\%t%\c$\Users\%r%\Favorites" "\\%z%\c$\source\profile\%r%\favorites"

XCOPY /E /C /R /I /K /Y /Q "\\%t%\c$\Users\%r%\Documents" "\\%z%\c$\source\profile\%r%\Documents"

echo F|XCOPY /E /C /R /I /K /Y /Q "\\%t%\c$\Users\%r%\AppData\Local\Google\Chrome\User Data\Default\Bookmarks" "\\%z%\c$\source\profile\%r%"

XCOPY /E /C /R /I /K /Y /Q "\\%t%\c$\Users\%r%\AppData\Roaming\Microsoft\Signatures" "\\%z%\c$\source\profile\%r%\Signatures"

XCOPY /E /C /R /I /K /Y /Q "\\%t%\c$\Users\%r%\Pictures" "\\%z%\c$\source\profile\%r%\Pictures"

if exist "\\%z%\C$\source\profile\%r%\Network.reg" del "\\%z%\C$\source\profile\%r%\Network.reg"

if exist "\\%z%\C$\source\profile\%r%\Printers.reg" del "\\%z%\C$\source\profile\%r%\Printers.reg"

REM wmic /node:%t% process call create "reg export \"HKEY_USERS\%myvar%\Network" "\\%z%\c$\source\profile\%r%\Network.reg" /y

REM wmic /node:%t% process call create "reg export \"HKEY_USERS\%myvar%\Printers\Connections\" "\\%z%\c$\source\profile\%r%\Printers.reg" /y

goto Output

:Output

pushd \\%z%\c$\

md Temp

pushd \\%z%\c$\Source\

md Profile
pushd "\\%z%\c$\Source\Profile"
ECHO CD C:\ > %r%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%r%\Desktop" "C:\Users\%r%\Desktop" >> %r%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%r%\Favorites" "C:\Users\%r%\Favorites" >> %r%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%r%\Documents" "C:\Users\%r%\Documents" >> %r%.bat
ECHO echo F|XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%r%\Bookmarks" "C:\Users\%r%\AppData\Local\Google\Chrome\User Data\Default" >> %r%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%r%\Signatures" "C:\Users\%r%\AppData\Roaming\Microsoft\Signatures" >> %r%.bat
ECHO XCOPY /E /C /R /I /K /Y /Q "C:\Source\Profile\%r%\Pictures" "C:\Users\%r%\Pictures" >> %r%.bat
ECHO taskkill /f /IM explorer.exe >> %r%.bat
ECHO start explorer.exe >> %r%.bat
ECHO start /b ^"^" cmd /c del ^"%%~f0^"^&exit /b >> %r%.bat

pushd "\\%z%\c$\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\"

ECHO @ECHO off > %r%.bat
ECHO if not exist C:\Users\%r% exit >> %r%.bat
ECHO if not exist "C:\source\profile\%r%.bat" exit >> %r%.bat
ECHO cd /d C:\ >> %r%.bat
ECHO ECHO Copying, please wait... >> %r%.bat
ECHO if exist "C:\source\profile\%r%\Network.reg" regedit /S "C:\source\profile\%r%\Network.reg" >> %r%.bat
ECHO if exist "C:\source\profile\%r%\Printers.reg" regedit /S "C:\source\profile\%r%\Printers.reg" >> %r%.bat
ECHO if exist "C:\source\profile\%r%.bat" "C:\source\profile\%r%.bat" >> %r%.bat
REM ECHO DEL /F/Q/S "C:\Source\Profile\%r%\desktop.ini" >> %r%.bat
ECHO ECHO. >> %r%.bat
ECHO ECHO Migration Complete >> %r%.bat
ECHO ECHO. >> %r%.bat
ECHO exit >> %r%.bat

net use * /d /y

goto start
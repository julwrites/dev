@echo off

ECHO -----------------------------------------------------------------------------------
ECHO       _____                                  ______               ______)          
ECHO      (, /      /)           ,               (, /    )            (, /        /)    
ECHO        /      // _   _ __    _/_  _  _        /    /  _ _ _        /  ______//  _  
ECHO    ___/__(_(_(/_ (_(/ / (__(_(___(/_/_)_    _/___ /__(/_(/__    ) /  (_)(_)(/_ /_)_
ECHO  /   /                                    (_/___ /             (_/                 
ECHO (__ /                                                                              
ECHO -----------------------------------------------------------------------------------

:: BatchGotAdmin
:-------------------------------------
:admin
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
IF '%errorlevel%' NEQ '0' (
    ECHO Requesting administrative privileges...
    GOTO UACPrompt
) ELSE ( GOTO gotAdmin )

:UACPrompt
    ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    SET params= %*
    ECHO UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    DEL "%temp%\getadmin.vbs"
    EXIT /B

:gotAdmin
    PUSHD "%CD%"
    CD /D "%~dp0"
:--------------------------------------    

:: BatchScriptProxy
:--------------------------------------    
:disableproxy
    SET TMP_HTTP_PROXY=%HTTP_PROXY%
    SET TMP_HTTPS_PROXY=%HTTPS_PROXY%
    SET TMP_NO_PROXY=%NO_PROXY%

    SET HTTP_PROXY=
    SET HTTPS_PROXY=
    SET NO_PROXY=
:--------------------------------------    

:: BatchScriptDeploy
:--------------------------------------    
:deploy
    CD %TEMP%

    ECHO Installing Chocolatey

    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

    CALL chocolatey upgrade chocolatey

    CALL choco install -y python

    DEL "%TEMP%\deploy.py"

    ECHO Downloading deploy script

    powershell -Command "Invoke-WebRequest https://raw.githubusercontent.com/julwrites/dev/master/deploy.py -OutFile %TEMP%\deploy.py"

    CALL python "%TEMP%\deploy.py"

    DEL "%TEMP%\deploy.py"

:: BatchScriptProxy
:--------------------------------------    
:restoreproxy
    SET HTTP_PROXY=%TMP_HTTP_PROXY%
    SET HTTPS_PROXY=%TMP_HTTPS_PROXY%
    SET NO_PROXY=%TMP_NO_PROXY%

    SET TMP_HTTP_PROXY=
    SET TMP_HTTPS_PROXY=
    SET TMP_NO_PROXY=
:--------------------------------------    

pause

EXIT /B
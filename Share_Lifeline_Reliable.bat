@echo off
COLOR 0A
TITLE Lifeline Reliable Link
ECHO.
ECHO ========================================================
ECHO      LIFELINE RELIABLE LINK GENERATOR
ECHO ========================================================
ECHO.
ECHO Connecting to reliable server...
ECHO.
ECHO Please wait for a line that says "https://......lhr.life"
ECHO COPY that link.
ECHO.
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -R 80:127.0.0.1:5000 nokey@localhost.run
PAUSE

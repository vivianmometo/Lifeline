@echo off
COLOR 0A
TITLE Lifeline Public Link Generator
ECHO.
ECHO ========================================================
ECHO         GENERATING NAMED LINK: LIFELINE-PHARMACY
ECHO ========================================================
ECHO.
ECHO Attempting to reserve specific name "lifeline-pharmacy"...
ECHO.
ECHO NOTE: If "lifeline-pharmacy" is taken, it might generate a random one
ECHO or fail. Keep this window OPEN.
ECHO.
ECHO --------------------------------------------------------
ECHO Trying Serveo.net (Custom Name)...
ECHO --------------------------------------------------------
ssh -o StrictHostKeyChecking=no -R lifeline-pharmacy:80:127.0.0.1:5000 serveo.net

ECHO.
ECHO --------------------------------------------------------
ECHO Serveo closed or failed. Trying Localhost.run (Random Name)...
ECHO --------------------------------------------------------
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:5000 nokey@localhost.run
PAUSE

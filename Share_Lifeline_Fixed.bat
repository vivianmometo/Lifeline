@echo off
COLOR 0B
TITLE Lifeline Sharing Tool (Fixed)
ECHO.
ECHO ========================================================
ECHO          LIFELINE SHARING TOOL (FIXED)
ECHO ========================================================
ECHO.
ECHO Option 1: Custom Name (lifeline-pharmacy) via Serveo
ECHO           (Often busy/down, but gives nice name)
ECHO.
ECHO Option 2: Random Name via Localhost.run
ECHO           (Very reliable, but random link name)
ECHO.
ECHO --------------------------------------------------------
ECHO Attempting Option 1 (Custom Name)...
ECHO If this freezes or says "Connection Refused", close and try Option 2.
ECHO --------------------------------------------------------
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -R lifeline-pharmacy:80:127.0.0.1:5000 serveo.net

ECHO.
ECHO --------------------------------------------------------
ECHO Option 1 failed or closed.
ECHO Swapping to Option 2 (Reliable Random Link)...
ECHO Please copy the link like "https://xxxxxx.localhost.run" below.
ECHO --------------------------------------------------------
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -R 80:127.0.0.1:5000 nokey@localhost.run

PAUSE

@echo off
echo ================================================================
echo MedTrust - Open Port 8000 in Windows Firewall
echo ================================================================
echo This allows other PCs, phones, and tablets on your Wi-Fi or LAN
echo network to access the MedTrust application.
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Administrator privileges required.
    echo Please right-click this file and select "Run as administrator".
    echo.
    pause
    exit /b 1
)

netsh advfirewall firewall show rule name="MedTrust LAN Port 8000" >nul 2>&1
if %errorLevel% equ 0 (
    echo [INFO] Firewall rule already exists. Updating...
    netsh advfirewall firewall delete rule name="MedTrust LAN Port 8000" >nul 2>&1
)

netsh advfirewall firewall add rule name="MedTrust LAN Port 8000" dir=in action=allow protocol=TCP localport=8000
echo.
echo [SUCCESS] Port 8000 is now open for incoming network connections!
echo Other devices on your Wi-Fi can now connect to this PC.
echo.
pause


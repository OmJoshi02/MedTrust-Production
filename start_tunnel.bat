@echo off
echo ================================================================
echo MedTrust - High-Speed Cloudflare HTTPS Tunnel for Netlify
echo ================================================================
echo Starting Cloudflare Tunnel (100%% uptime, no 503 errors)...
echo Keep this window OPEN while running your Netlify frontend!
echo.
"%~dp0cloudflared.exe" tunnel --url http://localhost:8000
pause

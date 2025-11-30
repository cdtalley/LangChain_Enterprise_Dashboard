@echo off
echo ========================================
echo Starting Next.js Enterprise Dashboard
echo ========================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting development server...
echo Open http://localhost:3000 in your browser
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

call npm run dev


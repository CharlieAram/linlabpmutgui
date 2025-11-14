#!/bin/bash
# Startup script for frontend application

echo "========================================="
echo "TX7332 PMUT Control - Starting Frontend"
echo "========================================="

cd frontend
echo "Starting React development server"
echo "Application will open at http://localhost:5173"
echo ""

npm run dev


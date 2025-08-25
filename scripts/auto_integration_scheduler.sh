#!/bin/bash
# 🚀 Automated Template Integration Scheduler
# EU-DSGVO & Menschenrechts-konform

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_DIR/logs/auto_integration.log"

# Erstelle Log-Verzeichnis
mkdir -p "$PROJECT_DIR/logs"

# Führe automatische Integration aus
echo "$(date): Starting automated template integration..." >> "$LOG_FILE"
cd "$PROJECT_DIR"
.venv/bin/python scripts/auto_template_integrator.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): Integration successful" >> "$LOG_FILE"
    
    # Commit und Push zu GitHub (wenn gewünscht)
    if [ -f ".git/config" ]; then
        git add .
        git commit -m "🤖 Automated template integration $(date)" || true
        git push origin main || true
    fi
else
    echo "$(date): Integration failed" >> "$LOG_FILE"
fi

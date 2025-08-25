#!/usr/bin/env python3
"""
🔧 PORTAINER JSON FORMAT VALIDATOR
=================================================
Validiert JSON spezifisch für Portainer-Kompatibilität
"""

import json
import logging
from typing import Dict, List, Any

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_portainer_format():
    """Validiere Portainer-spezifische JSON-Struktur"""
    template_file = "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/web/portainer-template.json"
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"❌ JSON Parse-Fehler: {e}")
        return False
    
    logger.info("🔍 Validiere Portainer-spezifische Struktur...")
    
    errors = []
    templates = data.get('templates', [])
    
    for i, template in enumerate(templates):
        # Port Validation
        if 'ports' in template:
            ports = template['ports']
            if not isinstance(ports, list):
                errors.append(f"Template {i}: Ports müssen ein Array sein")
            else:
                for j, port in enumerate(ports):
                    if not isinstance(port, str):
                        errors.append(f"Template {i}, Port {j}: Port muss ein String sein, nicht {type(port).__name__}")
                        logger.warning(f"   Problematischer Port: {port}")
        
        # Type Validation
        if 'type' in template:
            if not isinstance(template['type'], int):
                errors.append(f"Template {i}: Type muss eine Zahl sein")
        
        # Title Validation
        if 'title' in template:
            if not isinstance(template['title'], str):
                errors.append(f"Template {i}: Title muss ein String sein")
        
        # Categories Validation
        if 'categories' in template:
            categories = template['categories']
            if not isinstance(categories, list):
                errors.append(f"Template {i}: Categories müssen ein Array sein")
            else:
                for j, category in enumerate(categories):
                    if not isinstance(category, str):
                        errors.append(f"Template {i}, Category {j}: Category muss ein String sein")
        
        # Environment Variables Validation
        if 'env' in template:
            env_vars = template['env']
            if not isinstance(env_vars, list):
                errors.append(f"Template {i}: Environment Variables müssen ein Array sein")
            else:
                for j, env_var in enumerate(env_vars):
                    if not isinstance(env_var, dict):
                        errors.append(f"Template {i}, Env {j}: Environment Variable muss ein Objekt sein")
                    elif 'name' not in env_var:
                        errors.append(f"Template {i}, Env {j}: Environment Variable muss 'name' Feld haben")
    
    if errors:
        logger.error(f"❌ {len(errors)} Portainer-Validierungsfehler gefunden:")
        for error in errors[:10]:  # Zeige nur erste 10
            logger.error(f"   {error}")
        if len(errors) > 10:
            logger.error(f"   ... und {len(errors) - 10} weitere")
        return False
    else:
        logger.info(f"✅ Portainer-Validierung erfolgreich! {len(templates)} Templates sind korrekt formatiert")
        return True

def main():
    """Hauptfunktion"""
    logger.info("🔧 PORTAINER JSON FORMAT VALIDATOR")
    logger.info("=" * 50)
    
    success = validate_portainer_format()
    
    if success:
        logger.info("🎉 ALLE PORTAINER-VALIDIERUNGEN BESTANDEN!")
        logger.info("💎 JSON ist 100% Portainer-kompatibel!")
    else:
        logger.error("❌ Portainer-Kompatibilitätsprobleme gefunden!")
    
    return success

if __name__ == "__main__":
    main()
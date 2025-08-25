#!/usr/bin/env python3
"""
🔧 Automatischer Port-Format-Fixer für Portainer JSON
Behebt alle Port-Formatierungsprobleme für Go struct compatibility
"""

import json
import logging
import sys
from pathlib import Path

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fix_port_format(port_item):
    """Konvertiert Port-Objekt zu korrektem String-Format"""
    if isinstance(port_item, dict):
        # Wenn es ein Dictionary ist, konvertiere zu String-Array
        ports = []
        for key, value in port_item.items():
            # Extrahiere Port-Info aus value (z.B. "8086:8086/tcp")
            ports.append(value)
        return ports
    elif isinstance(port_item, str):
        return port_item
    else:
        logging.warning(f"⚠️ Unerwarteter Port-Typ: {type(port_item)}")
        return str(port_item)

def fix_ports_in_template(template, template_idx):
    """Behebt alle Port-Probleme in einem Template"""
    fixed = False
    
    if 'ports' in template and isinstance(template['ports'], list):
        new_ports = []
        for port_idx, port in enumerate(template['ports']):
            if isinstance(port, dict):
                logging.info(f"🔧 Behebe Port in Template {template_idx}, Port {port_idx}: {port}")
                fixed_port = fix_port_format(port)
                if isinstance(fixed_port, list):
                    new_ports.extend(fixed_port)
                else:
                    new_ports.append(fixed_port)
                fixed = True
            else:
                new_ports.append(port)
        
        if fixed:
            template['ports'] = new_ports
            logging.info(f"✅ Template {template_idx} Ports behoben: {new_ports}")
    
    return fixed

def main():
    """Hauptfunktion zum Beheben aller Port-Formate"""
    logging.info("🔧 AUTOMATISCHER PORT-FORMAT-FIXER")
    logging.info("=" * 50)
    
    template_file = Path("web/portainer-template.json")
    
    if not template_file.exists():
        logging.error(f"❌ Template-Datei nicht gefunden: {template_file}")
        return False
    
    # Backup erstellen
    backup_file = template_file.with_suffix('.backup.json')
    logging.info(f"💾 Erstelle Backup: {backup_file}")
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        templates = data.get('templates', [])
        fixes_applied = 0
        
        logging.info(f"🔍 Analysiere {len(templates)} Templates...")
        
        for idx, template in enumerate(templates):
            if fix_ports_in_template(template, idx):
                fixes_applied += 1
        
        if fixes_applied > 0:
            # Speichere die korrigierte Datei
            logging.info(f"💾 Speichere korrigierte Template-Datei...")
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"✅ {fixes_applied} Port-Formate erfolgreich behoben!")
            
            # Validiere JSON-Syntax
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                logging.info("✅ JSON-Syntax ist gültig!")
            except json.JSONDecodeError as e:
                logging.error(f"❌ JSON-Syntax-Fehler nach Korrektur: {e}")
                return False
        else:
            logging.info("✅ Keine Port-Format-Probleme gefunden!")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Fehler beim Beheben der Port-Formate: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
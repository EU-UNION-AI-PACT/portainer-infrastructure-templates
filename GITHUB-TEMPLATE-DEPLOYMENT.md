# 🚀 GitHub Repository Template Setup

## 📁 **Repository Struktur (Empfohlen)**

```
portainer-templates/
├── README.md
├── portainer-template.json          # Haupt-Template Datei
├── stacks/                          # Stack Definitionen
│   ├── security/
│   │   ├── eu-gdpr-security.yml
│   │   ├── extended-security.yml
│   │   └── monitoring-stack.yml
│   ├── databases/
│   │   ├── database-complete.yml
│   │   ├── database-relational.yml
│   │   └── database-nosql.yml
│   └── development/
│       ├── development-stack.yml
│       └── free-alternatives.yml
├── docs/                            # GitHub Pages
│   └── index.html
└── .github/
    └── workflows/
        └── validate-templates.yml    # CI/CD Validation
```

## 🎯 **Setup-Optionen**

### **Option 1: GitHub Pages (Professionell)**

1. **Repository erstellen**: `portainer-templates`
2. **GitHub Pages aktivieren**: Settings → Pages → Source: GitHub Actions
3. **Template URL**: `https://username.github.io/portainer-templates/portainer-template.json`

**Vorteile:**
- ✅ **HTTPS SSL** (sicher)
- ✅ **CDN Performance** (schnell)
- ✅ **Custom Domain** möglich
- ✅ **Versionierung** mit Git
- ✅ **CI/CD Validation**

### **Option 2: GitHub Raw (Einfach)**

1. **Repository erstellen**: `portainer-templates`
2. **Template hochladen**: `portainer-template.json` → main branch
3. **Template URL**: `https://raw.githubusercontent.com/username/portainer-templates/main/portainer-template.json`

**Vorteile:**
- ✅ **Sofort verfügbar** (keine Konfiguration)
- ✅ **Einfacher Upload**
- ✅ **Automatische Updates**

## 🔧 **Automatisierte Deployment-Pipeline**

### **GitHub Actions Workflow** (`.github/workflows/deploy.yml`):

```yaml
name: Deploy Portainer Templates
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Validate JSON
      run: |
        jq empty portainer-template.json
        echo "✅ JSON validation passed"
    
    - name: Validate Template Structure
      run: |
        TEMPLATE_COUNT=$(jq '.templates | length' portainer-template.json)
        echo "📊 Templates found: $TEMPLATE_COUNT"
        
        # Validate required fields
        jq -r '.templates[] | select(.title == null or .description == null)' portainer-template.json
        if [ $? -eq 0 ]; then
          echo "❌ Invalid template structure"
          exit 1
        fi
        echo "✅ Template structure validation passed"
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

## 📋 **Deployment Commands**

### **1. Repository Setup**
```bash
# Neues Repository erstellen
git init portainer-templates
cd portainer-templates

# Template-Dateien kopieren
cp "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/portainer-template.json" .
cp -r "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/stacks" .

# GitHub Repository erstellen und pushen
git add .
git commit -m "🚀 Initial Portainer Templates Setup"
git branch -M main
git remote add origin https://github.com/username/portainer-templates.git
git push -u origin main
```

### **2. GitHub Pages Aktivierung**
```bash
# GitHub CLI (falls installiert)
gh repo create portainer-templates --public
gh api repos/:owner/:repo/pages -f source[branch]=main -f source[path]=/

# Oder manuell über GitHub Web Interface:
# 1. Settings → Pages
# 2. Source: Deploy from a branch
# 3. Branch: main / (root)
```

## 🎯 **Portainer Integration**

### **Template URLs für Portainer:**

1. **GitHub Pages** (Empfohlen):
   ```
   https://username.github.io/portainer-templates/portainer-template.json
   ```

2. **GitHub Raw**:
   ```
   https://raw.githubusercontent.com/username/portainer-templates/main/portainer-template.json
   ```

3. **Kombiniert mit Official**:
   ```
   URL 1: https://raw.githubusercontent.com/portainer/templates/v3/templates.json
   URL 2: https://username.github.io/portainer-templates/portainer-template.json
   ```

## 🚀 **Vorteile der GitHub-Lösung**

### **Für Unternehmen:**
- ✅ **Professional Image** (github.io Domain)
- ✅ **SSL/HTTPS** (Sicherheit)
- ✅ **99.9% Uptime** (GitHub Infrastructure)
- ✅ **Globale CDN** (Performance)

### **Für Entwicklung:**
- ✅ **Versionskontrolle** (Git History)
- ✅ **Branching** (dev/staging/prod)
- ✅ **Pull Requests** (Code Review)
- ✅ **Issues & Documentation**

### **Für Wartung:**
- ✅ **Automatische Validation** (CI/CD)
- ✅ **Rollback-Fähigkeit** (Git)
- ✅ **Kollaboration** (Team Access)
- ✅ **Monitoring** (GitHub Insights)

## 🎪 **Template-Ökosystem Erweitern**

```
Haupt-Repository: portainer-templates
├── portainer-template.json (125 Templates)
├── specialized/
│   ├── database-templates.json (118 DB Templates)
│   ├── security-templates.json (7 Security Templates)
│   └── development-templates.json (Dev Templates)
└── regions/
    ├── eu-gdpr-templates.json (EU-konform)
    └── us-templates.json (US-optimiert)
```

---

**💡 Empfehlung**: Verwende **GitHub Pages** für maximale Professionalität und Performance!

*Template Count: 125 | Format: Portainer v3 | Status: Production Ready*
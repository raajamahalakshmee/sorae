# Sorae Web App ☕

A modern, coffee-themed passwordless authentication web app for Sorae.

## 🚀 Quick Start

1. **Install requirements** (Flask is already in your backend venv):
   ```bash
   pip install flask
   ```

2. **Set environment variables for email:**
   ```powershell
   $env:EMAIL_FROM="sorae.net@gmail.com"
   $env:EMAIL_PASSWORD="<your-app-password>"
   $env:SMTP_SERVER="smtp.gmail.com"
   $env:SMTP_PORT="587"
   $env:FLASK_SECRET_KEY="your-secret-key"
   ```
   Replace `<your-app-password>` with your Gmail app password for sorae.net@gmail.com.

3. **Run the web app:**
   ```bash
   python app.py
   ```
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

## 🎨 Coffee Color Theme
- Dark Coffee: #4B2E2B
- Medium Coffee: #7B4B3A
- Latte Cream: #D7C0AE
- Milk Foam: #F5EFE6
- Accent: #A47149

## ✉️ Email Setup
- All magic links are sent from `sorae.net@gmail.com`.
- Uses secure Gmail SMTP with app password.
- Update `EMAIL_FROM` and `EMAIL_PASSWORD` as needed.

## 🛠️ Features
- Onboarding (register with email)
- Magic link login
- Coffee-inspired, modern UI
- Dashboard (more features coming soon)

## 📦 Project Structure
```
web/
  app.py
  templates/
    base.html
    home.html
    register.html
    login.html
    dashboard.html
  static/
    coffee.css
```

## 📝 To Do
- Add backup code management
- Add login history
- Add account recovery
- Add admin panel

---
Enjoy your secure, coffee-inspired authentication experience with Sorae! ☕

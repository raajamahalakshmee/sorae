from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from utils.email_service import email_service

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Onboarding (register)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        # Simulate sending magic link
        token = os.urandom(4).hex()
        session['pending_email'] = email
        session['pending_token'] = token
        email_service.send_magic_link(email, token)
        flash('Magic link sent! Please check your inbox.', 'info')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login (magic link token)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = request.form.get('token')
        if token == session.get('pending_token'):
            # In demo: always succeed biometrics
            session['authenticated'] = True
            flash('Login successful! Welcome to Sorae.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid token. Please try again.', 'danger')
    return render_template('login.html')

# Dashboard (protected)
@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', email=session.get('pending_email'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

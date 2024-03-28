from .app.blueprints.main import main
from flask import Flask, request, render_template, jsonify, redirect, url_for
import requests
from app import Gym, query_gym, db, app, login, login_manager
from flask_login import current_user, logout_user, login_required


google_places_api_key = 'AIzaSyAx4rIxHCzyy8AtTBdrbA5NL1VL57pSJ4E'

@main.route('/')
def alpha_app():
    return "<p>Hello, Alpha! Welcome to your World!</p>"

@main.route('/user/<name>')
def user(name):
    return f'Hello, {name}! Welcome to your World!'

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return f'Login successful for user: {email} {password}'
    else:
        return render_template('login.html')

def search(gym):
    query = request.form.get('query')
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?key={google_places_api_key}&query={query}+gym'
    response = requests.get(url)
    data = response.json()
    
    gyms = []
    for result in data.get('results', []):
        gym = {
            'name': result.get('name'),
            'address': result.get('formatted_address'),
            'hours': result.get('opening_hours', {}).get('weekday_text', []),
            'phone': result.get('formatted_phone_number'),
            'photo_reference': result.get('photos', [])[0].get('photo_reference') if result.get('photos') else None
        }
        return gym
    else:
        return gyms.append

@main.route('/gymsearch', methods=['GET', 'POST'])
def GymSearch():
    if request.method == 'POST':
        gym = request.form.get('gym').lower()
        
    else:
        return render_template('gymsearch.html')
    
    
@main.route('/add_gym/<name>', methods=['GET', 'POST'])
@login_required
def add_gym(name):
    print(name)
    gym = Gym.query.filter_by(name=gym).first()
    if len(current_user.gyms.all()) < 5 and query_gym not in current_user.gyms.all():
        current_user.gyms.append(gym)
        db.session.commit()
        return redirect(url_for('main.gyms'))
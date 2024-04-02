from app.blueprints.main import main
from flask import request, render_template, redirect, url_for
import requests
from app import db
from flask_login import current_user, login_required
from app.models import Gym


API_KEY = 'AIzaSyBwyu5uGGOf2N3McdwS68EJAWaGDHK6tko'

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
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?key={API_KEY}&query={query}+gym'
    response = requests.get(url)
    data = response.json()
    print(data)
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
        name = request.form.get('name').lower()

        query_gym = Gym.query.filter_by(name=name).first()
        if query_gym:
            return render_template('gymsearch.html', gym=query_gym)
        gym = search(name)
        new_gym = Gym(name, gym['address'], gym['hours'], gym['phone'], gym['photo_reference'])
        new_gym.save()
        return render_template('gymsearch.html', gyms=gym)
    else:
        return render_template('gymsearch.html')
    
    
@main.route('/add_gym/<name>', methods=['GET', 'POST'])
@login_required
def add_gym(name):
    print(name)
    gym = Gym.query.filter_by(name=name).first()
    if len(current_user.gyms.all()) < 5 and gym not in current_user.gyms.all():
        current_user.gyms.append(gym)
        db.session.commit()
        return redirect(url_for('main.gyms'))

@main.route('/gyms')
@login_required
def gyms():
    return render_template('gyms.html', gyms=current_user.gyms.all())

@main.route('/remove_gym/<name>', methods=['GET', 'POST'])
@login_required
def remove_gym(name):
    gym = Gym.query.filter_by(name=name).first()
    if gym in current_user.gyms.all():
        current_user.gyms.remove(gym)
        db.session.commit()
        return redirect(url_for('main.gyms'))
    

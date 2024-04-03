from app.blueprints.main import main
from flask import request, render_template, redirect, url_for, jsonify
import requests
from app import db
from flask_login import current_user, login_required
from app.models import User, Workout
from random import choice



url = "https://gym-fit.p.rapidapi.com/exercises/search"

headers = {
	"X-RapidAPI-Key": "a6cd4199afmshef2cb6b483c6115p14bd76jsn974ac5d50912",
	"X-RapidAPI-Host": "gym-fit.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())

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

# def search(gym):
#     query = request.form.get('query')
#     url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?key={API_KEY}&query={query}+gym'
#     response = requests.get(url)
#     data = response.json()
#     print(data)
#     gyms = []
#     for result in data.get('results', []):
#         gym = {
#             'name': result.get('name'),
#             'address': result.get('formatted_address'),
#             'hours': result.get('opening_hours', {}).get('weekday_text', []),
#             'phone': result.get('formatted_phone_number'),
#             'photo_reference': result.get('photos', [])[0].get('photo_reference') if result.get('photos') else None
#         }
#         return gym
#     else:
#         return gyms.append

# @main.route('/gymsearch', methods=['GET', 'POST'])
# def GymSearch():
#     if request.method == 'POST':
#         name = request.form.get('name').lower()

#         query_gym = Gym.query.filter_by(name=name).first()
#         if query_gym:
#             return render_template('gymsearch.html', gym=query_gym)
#         gym = search(name)
#         new_gym = Gym(name, gym['address'], gym['hours'], gym['phone'], gym['photo_reference'])
#         new_gym.save()
#         return render_template('gymsearch.html', gyms=gym)
#     else:
#         return render_template('gymsearch.html')

# @main.route('/exercises', methods=['GET', 'POST'])
def get_exercises():
    url = "https://gym-fit.p.rapidapi.com/exercises/search"
    headers = {
        "X-RapidAPI-Key": "a6cd4199afmshef2cb6b483c6115p14bd76jsn974ac5d50912",
        "X-RapidAPI-Host": "gym-fit.p.rapidapi.com"
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)
        # Extract relevant information from the response
        exercises = {}
        for exercise in data:
            body_part = exercise['bodyParts']
            name = exercise['name']
            if len(body_part) > 1:
                for parts in body_part:
                    if parts not in exercises:
                        exercises[parts] = []
                    exercises[parts].append(name)
            if len(body_part) == 1:
                body_part = body_part[0]
            
            # if body_part not in exercises:
                    
            #     exercises[body_part]= []
            # exercises[body_part].append(name)

        return exercises
    else:
        return({'error': 'Failed to retrieve exercise data'})
    
    # @main.route('/exercisesearch', methods=['GET', 'POST'])
    # def ExerciseSearch():
    #     if request.method == 'POST':
    #         body_part = request.form.get('body_part').lower()

    #         query_exercise = Exercise.query.filter_by(body_part=body_part).first()
    #         if query_exercise:
    #             return render_template('workoutsearch.html', exercise=query_exercise)
    #         exercise = get_exercises(name)
    #         new_exercise = Exercise(name, body_part, exercise['instructions'])
    #         new_exercise.save()
    #         return render_template('workoutsearch.html', exercises=exercise)
    #     else:
    #         return render_template('workoutsearch.html')
@main.route('/exercisesearch', methods=['GET', 'POST'])
def ExerciseSearch():
    if request.method == 'POST':
        body_part = request.form.get('body_part')

        query_exercise = Workout.query.filter_by(body_part=body_part).first()
        if query_exercise:
            return render_template('workoutsearch.html', exercise=query_exercise)
        else:
            exercise = get_exercises()
            print(f"THIS IS A TEST {exercise[body_part]}")
            exercise = exercise[body_part]
            my_excercise = choice(exercise)
            return render_template('workoutsearch.html', exercises=exercise)
    else:
        return render_template('workoutsearch.html')
    
    
@main.route('/add_workout/<name>', methods=['GET', 'POST'])
@login_required
def add_workout(name):
    print(name)
    workout = workout.query.filter_by(name=name).first()
    if len(current_user.gyms.all()) < 5 and workout not in current_user.gyms.all():
        current_user.gyms.append(workout)
        db.session.commit()
        return redirect(url_for('main.workouts'))

@main.route('/workouts')
@login_required
def workouts():
    return render_template('workouts.html', workouts=current_user.workouts.all())

@main.route('/remove_workout/<name>', methods=['GET', 'POST'])
@login_required
def remove_workout(name):
    workout = workout.query.filter_by(name=name).first()
    if workout in current_user.workouts.all():
        current_user.workouts.remove(workout)
        db.session.commit()
        return redirect(url_for('main.workouts'))
    

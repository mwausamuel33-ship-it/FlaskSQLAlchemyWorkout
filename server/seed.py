#!/usr/bin/env python3
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import datetime, timedelta

with app.app_context():
    db.drop_all()
    db.create_all()

    ex1 = Exercise(name="Push-ups", category="strength", equipment_needed=False)
    ex2 = Exercise(name="Squats", category="strength", equipment_needed=False)
    ex3 = Exercise(name="Deadlifts", category="strength", equipment_needed=True)
    ex4 = Exercise(name="Running", category="cardio", equipment_needed=False)
    ex5 = Exercise(name="Cycling", category="cardio", equipment_needed=True)
    ex6 = Exercise(name="Yoga", category="flexibility", equipment_needed=False)
    ex7 = Exercise(name="Plank", category="strength", equipment_needed=False)
    ex8 = Exercise(name="Jumping Jacks", category="cardio", equipment_needed=False)

    exercises = [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8]
    for e in exercises: db.session.add(e)
    db.session.commit()

    today = datetime.now().date()
    w1 = Workout(date=today - timedelta(days=3), duration_minutes=45, notes="Upper body day")
    w2 = Workout(date=today - timedelta(days=2), duration_minutes=30, notes="Cardio session")
    w3 = Workout(date=today - timedelta(days=1), duration_minutes=60, notes="Full body")
    w4 = Workout(date=today, duration_minutes=40, notes="Core workout")

    workouts = [w1, w2, w3, w4]
    for w in workouts: db.session.add(w)
    db.session.commit()

    we1 = WorkoutExercise(workout_id=1, exercise_id=1, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=1, exercise_id=7, sets=3, duration_seconds=60)
    we3 = WorkoutExercise(workout_id=2, exercise_id=4, sets=1, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=3, exercise_id=1, reps=12, sets=3)
    we5 = WorkoutExercise(workout_id=3, exercise_id=2, reps=20, sets=3)
    we6 = WorkoutExercise(workout_id=3, exercise_id=3, reps=8, sets=4)
    we7 = WorkoutExercise(workout_id=4, exercise_id=7, sets=3, duration_seconds=90)
    we8 = WorkoutExercise(workout_id=4, exercise_id=6, sets=1, duration_seconds=2400)

    wes = [we1, we2, we3, we4, we5, we6, we7, we8]
    for we in wes: db.session.add(we)
    db.session.commit()

    print("Done!")
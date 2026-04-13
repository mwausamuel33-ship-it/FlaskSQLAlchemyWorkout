#!/usr/bin/env python3
# seed.py - adds sample data to the database
# WARNING: wipes the db first, so dont run on real data

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import datetime, timedelta

with app.app_context():

    print("Clearing database...")
    db.drop_all()
    db.create_all()

    # -- exercises --
    print("Seeding exercises...")

    exercise1 = Exercise(name="Push-ups",     category="strength",    equipment_needed=False)
    exercise2 = Exercise(name="Squats",        category="strength",    equipment_needed=False)
    exercise3 = Exercise(name="Deadlifts",     category="strength",    equipment_needed=True)
    exercise4 = Exercise(name="Running",       category="cardio",      equipment_needed=False)
    exercise5 = Exercise(name="Cycling",       category="cardio",      equipment_needed=True)
    exercise6 = Exercise(name="Yoga",          category="flexibility", equipment_needed=False)
    exercise7 = Exercise(name="Plank",         category="strength",    equipment_needed=False)
    exercise8 = Exercise(name="Jumping Jacks", category="cardio",      equipment_needed=False)

    all_exercises = [
        exercise1, exercise2, exercise3, exercise4,
        exercise5, exercise6, exercise7, exercise8
    ]

    for ex in all_exercises:
        db.session.add(ex)

    db.session.commit()  # commit so ids are assigned before we use them below
    print(f"  Added {len(all_exercises)} exercises")

    # -- workouts --
    print("Seeding workouts...")

    today = datetime.now().date()

    workout1 = Workout(date=today - timedelta(days=3), duration_minutes=45, notes="Upper body day")
    workout2 = Workout(date=today - timedelta(days=2), duration_minutes=30, notes="Cardio session")
    workout3 = Workout(date=today - timedelta(days=1), duration_minutes=60, notes="Full body")
    workout4 = Workout(date=today,                     duration_minutes=40, notes="Core workout")

    all_workouts = [workout1, workout2, workout3, workout4]

    for w in all_workouts:
        db.session.add(w)

    db.session.commit()
    print(f"  Added {len(all_workouts)} workouts")

    # -- workout exercises --
    # linking exercises to workouts
    # using raw ids because i know the insert order from above
    print("Seeding workout exercises...")

    # workout 1: push-ups + plank
    we1 = WorkoutExercise(workout_id=1, exercise_id=1, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=1, exercise_id=7, sets=3, duration_seconds=60)

    # workout 2: 30min run
    we3 = WorkoutExercise(workout_id=2, exercise_id=4, sets=1, duration_seconds=1800)

    # workout 3: push-ups, squats, deadlifts
    we4 = WorkoutExercise(workout_id=3, exercise_id=1, reps=12, sets=3)
    we5 = WorkoutExercise(workout_id=3, exercise_id=2, reps=20, sets=3)
    we6 = WorkoutExercise(workout_id=3, exercise_id=3, reps=8,  sets=4)

    # workout 4: plank + yoga
    we7 = WorkoutExercise(workout_id=4, exercise_id=7, sets=3, duration_seconds=90)
    we8 = WorkoutExercise(workout_id=4, exercise_id=6, sets=1, duration_seconds=2400)

    all_wes = [we1, we2, we3, we4, we5, we6, we7, we8]

    for we in all_wes:
        db.session.add(we)

    db.session.commit()
    print(f"  Added {len(all_wes)} workout exercises")

    print("\nDone! Database is ready.")

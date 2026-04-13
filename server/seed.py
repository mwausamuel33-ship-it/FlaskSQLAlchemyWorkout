#!/usr/bin/env python3
"""
Seed script to populate the database with sample data.
Run with: python seed.py
"""

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import datetime, timedelta

with app.app_context():
    # Clear existing data
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # Create sample exercises
    print("Creating exercises...")
    exercises = [
        Exercise(name="Push-ups", category="strength", equipment_needed=False),
        Exercise(name="Squats", category="strength", equipment_needed=False),
        Exercise(name="Deadlifts", category="strength", equipment_needed=True),
        Exercise(name="Running", category="cardio", equipment_needed=False),
        Exercise(name="Cycling", category="cardio", equipment_needed=True),
        Exercise(name="Yoga", category="flexibility", equipment_needed=False),
        Exercise(name="Plank", category="strength", equipment_needed=False),
        Exercise(name="Jumping Jacks", category="cardio", equipment_needed=False),
    ]
    
    for exercise in exercises:
        db.session.add(exercise)
    db.session.commit()
    print(f"Created {len(exercises)} exercises")

    # Create sample workouts
    print("Creating workouts...")
    today = datetime.now().date()
    workouts = [
        Workout(
            date=today - timedelta(days=3),
            duration_minutes=45,
            notes="Upper body strength training"
        ),
        Workout(
            date=today - timedelta(days=2),
            duration_minutes=30,
            notes="Cardio session"
        ),
        Workout(
            date=today - timedelta(days=1),
            duration_minutes=60,
            notes="Full body workout"
        ),
        Workout(
            date=today,
            duration_minutes=40,
            notes="Core and flexibility"
        ),
    ]
    
    for workout in workouts:
        db.session.add(workout)
    db.session.commit()
    print(f"Created {len(workouts)} workouts")

    # Create workout exercises (associations)
    print("Creating workout exercises...")
    workout_exercises = [
        # Workout 1: Upper body
        WorkoutExercise(
            workout_id=1,
            exercise_id=1,  # Push-ups
            reps=15,
            sets=3,
            duration_seconds=None
        ),
        WorkoutExercise(
            workout_id=1,
            exercise_id=7,  # Plank
            reps=None,
            sets=3,
            duration_seconds=60
        ),
        # Workout 2: Cardio
        WorkoutExercise(
            workout_id=2,
            exercise_id=4,  # Running
            reps=None,
            sets=1,
            duration_seconds=1800  # 30 minutes
        ),
        # Workout 3: Full body
        WorkoutExercise(
            workout_id=3,
            exercise_id=1,  # Push-ups
            reps=12,
            sets=3,
            duration_seconds=None
        ),
        WorkoutExercise(
            workout_id=3,
            exercise_id=2,  # Squats
            reps=20,
            sets=3,
            duration_seconds=None
        ),
        WorkoutExercise(
            workout_id=3,
            exercise_id=3,  # Deadlifts
            reps=8,
            sets=4,
            duration_seconds=None
        ),
        # Workout 4: Core and flexibility
        WorkoutExercise(
            workout_id=4,
            exercise_id=7,  # Plank
            reps=None,
            sets=3,
            duration_seconds=90
        ),
        WorkoutExercise(
            workout_id=4,
            exercise_id=6,  # Yoga
            reps=None,
            sets=1,
            duration_seconds=2400  # 40 minutes
        ),
    ]
    
    for we in workout_exercises:
        db.session.add(we)
    db.session.commit()
    print(f"Created {len(workout_exercises)} workout exercises")

    print("Database seeding completed successfully!")
    
    # Print summary
    print("\n=== Database Summary ===")
    print(f"Total exercises: {Exercise.query.count()}")
    print(f"Total workouts: {Workout.query.count()}")
    print(f"Total workout exercises: {WorkoutExercise.query.count()}")

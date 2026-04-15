# models.py - database tables as python classes
# SQLAlchemy maps each class to a table automatically

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# db instance - connected to the app in app.py with db.init_app(app)
db = SQLAlchemy()


# Exercise - a type of exercise like push-ups or running
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # middle table between workouts and exercises
    # cascade means related workout_exercises get deleted if this exercise is deleted
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    # goes through the join table - i had to look up what overlaps does
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        overlaps='exercises,workout_exercises'
    )






# Workout - a single workout session on a specific day
class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)  # optional

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        overlaps='exercises,workout_exercises'
    )






# WorkoutExercise - join table between Workout and Exercise
# also stores reps/sets/duration for each exercise in each workout
# this was the hardest part to understand tbh
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    # all optional - strength exercises use reps+sets, cardio uses duration
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id'),  # no duplicates
        db.CheckConstraint('reps IS NULL OR reps > 0'),
        db.CheckConstraint('sets IS NULL OR sets > 0'),
        db.CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0'),
    )

    workout = db.relationship(
        'Workout',
        back_populates='workout_exercises',
        overlaps='exercises,workouts'
    )

    exercise = db.relationship(
        'Exercise',
        back_populates='workout_exercises',
        overlaps='exercises,workouts'
    )

    # one validator covers reps, sets, and duration_seconds
    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_numbers(self, key, value):
        if value != None and value <= 0:
            raise ValueError(f'{key} must be a positive number')
        return value

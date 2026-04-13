from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()


class Exercise(db.Model):
    """Exercise model representing a reusable exercise template."""
    __tablename__ = 'exercises'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan',
        lazy=True
    )
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        lazy=True,
        overlaps='exercises,workout_exercises'
    )

    # Model Validations
    @validates('name')
    def validate_name(self, key, value):
        """Validate that exercise name is not empty."""
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError('Exercise name cannot be empty')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        """Validate that category is from allowed values."""
        allowed_categories = ['strength', 'cardio', 'flexibility', 'balance']
        if not value or value not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return value

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    """Workout model representing a workout session."""
    __tablename__ = 'workouts'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationships
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan',
        lazy=True
    )
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        lazy=True,
        overlaps='exercises,workout_exercises'
    )

    # Model Validations
    @validates('date')
    def validate_date(self, key, value):
        """Validate that date is provided."""
        if not value:
            raise ValueError('Workout date is required')
        return value

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        """Validate that duration_minutes is positive."""
        if value is None:
            raise ValueError('Duration minutes is required')
        if not isinstance(value, int) or value <= 0:
            raise ValueError('Duration minutes must be a positive integer')
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    """Join table representing an exercise within a workout."""
    __tablename__ = 'workout_exercises'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises', overlaps='exercises,workouts')
    exercise = db.relationship('Exercise', back_populates='workout_exercises', overlaps='exercises,workouts')

    # Unique constraint to prevent duplicate exercise-workout combinations
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),
        db.CheckConstraint('reps IS NULL OR reps > 0', name='check_reps_positive'),
        db.CheckConstraint('sets IS NULL OR sets > 0', name='check_sets_positive'),
        db.CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='check_duration_positive'),
    )

    # Model Validations
    @validates('workout_id')
    def validate_workout_id(self, key, value):
        """Validate that workout_id exists."""
        if not value:
            raise ValueError('Workout ID is required')
        return value

    @validates('exercise_id')
    def validate_exercise_id(self, key, value):
        """Validate that exercise_id exists."""
        if not value:
            raise ValueError('Exercise ID is required')
        return value

    @validates('reps')
    def validate_reps(self, key, value):
        """Validate that reps is positive if provided."""
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Reps must be a positive integer')
        return value

    @validates('sets')
    def validate_sets(self, key, value):
        """Validate that sets is positive if provided."""
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Sets must be a positive integer')
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        """Validate that duration_seconds is positive if provided."""
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError('Duration seconds must be a positive integer')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: workout={self.workout_id}, exercise={self.exercise_id}>'

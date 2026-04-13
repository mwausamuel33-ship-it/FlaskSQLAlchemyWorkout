from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from models import db, Workout, Exercise, WorkoutExercise
from datetime import datetime


class WorkoutExerciseSchema(Schema):
    """Schema for WorkoutExercise serialization and deserialization."""
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1, error='Reps must be a positive integer'))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1, error='Sets must be a positive integer'))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1, error='Duration seconds must be a positive integer'))

    # Schema validations
    @validates('workout_id')
    def validate_workout_exists(self, value):
        """Validate that the workout exists."""
        if value and not Workout.query.get(value):
            raise ValidationError('Workout does not exist')

    @validates('exercise_id')
    def validate_exercise_exists(self, value):
        """Validate that the exercise exists."""
        if value and not Exercise.query.get(value):
            raise ValidationError('Exercise does not exist')

    @post_load
    def create_object(self, data, **kwargs):
        """Create WorkoutExercise object from validated data."""
        # Check for duplicate exercise in workout
        existing = WorkoutExercise.query.filter_by(
            workout_id=data['workout_id'],
            exercise_id=data['exercise_id']
        ).first()
        if existing:
            raise ValidationError({'error': 'This exercise is already added to this workout'})
        
        return WorkoutExercise(**data)

    class Meta:
        model = WorkoutExercise


class ExerciseSchema(Schema):
    """Schema for Exercise serialization and deserialization."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error='Name cannot be empty'))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['strength', 'cardio', 'flexibility', 'balance'],
            error='Category must be one of: strength, cardio, flexibility, balance'
        )
    )
    equipment_needed = fields.Bool(missing=False)
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, dump_only=True)

    # Schema validations
    @validates('name')
    def validate_unique_name(self, value):
        """Validate that exercise name is unique."""
        if value:
            existing = Exercise.query.filter_by(name=value.strip()).first()
            if existing:
                raise ValidationError('An exercise with this name already exists')

    @post_load
    def create_object(self, data, **kwargs):
        """Create Exercise object from validated data."""
        return Exercise(**data)

    class Meta:
        model = Exercise


class WorkoutSchema(Schema):
    """Schema for Workout serialization and deserialization."""
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error='Duration must be a positive integer')
    )
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True, dump_only=True)

    # Schema validations
    @validates('date')
    def validate_date_not_future(self, value):
        """Validate that date is not in the future."""
        if value and value > datetime.now().date():
            raise ValidationError('Workout date cannot be in the future')

    @post_load
    def create_object(self, data, **kwargs):
        """Create Workout object from validated data."""
        return Workout(**data)

    class Meta:
        model = Workout

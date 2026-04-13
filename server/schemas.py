# schemas.py - marshmallow schemas for validation + serialization
#
# quick note on load vs dump (i kept mixing these up):
#   load()  = JSON dict -> python object  (incoming request data)
#   dump()  = python object -> JSON dict  (outgoing response data)

from marshmallow import Schema, fields, validate, validates, ValidationError
from models import db, Workout, Exercise, WorkoutExercise


# defined first because the other schemas reference it with fields.Nested()
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)  # assigned by db, not needed in input
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    @validates('workout_id')
    def validate_workout_id(self, value):
        found = Workout.query.get(value)
        if found == None:
            raise ValidationError('No workout found with that id')

    @validates('exercise_id')
    def validate_exercise_id(self, value):
        found = Exercise.query.get(value)
        if found == None:
            raise ValidationError('No exercise found with that id')

    class Meta:
        model = WorkoutExercise


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    # validate.OneOf checks against a list of allowed values
    category = fields.Str(
        required=True,
        validate=validate.OneOf(['strength', 'cardio', 'flexibility', 'balance'])
    )
    equipment_needed = fields.Bool(missing=False)  # defaults to False if not sent
    workout_exercises = fields.Nested(
        'WorkoutExerciseSchema', many=True, dump_only=True
    )

    class Meta:
        model = Exercise


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)  # marshmallow converts string to date object
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.Nested(
        'WorkoutExerciseSchema', many=True, dump_only=True
    )

    class Meta:
        model = Workout

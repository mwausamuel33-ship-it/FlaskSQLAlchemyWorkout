from flask import Flask, request
from flask_migrate import Migrate
from models import *
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

@app.route('/')
def home():
    return {
        'message': 'Workout Tracker API',
        'version': '1.0',
        'endpoints': {
            'workouts': {
                'GET /workouts': 'Get all workouts',
                'GET /workouts/<id>': 'Get specific workout',
                'POST /workouts': 'Create new workout',
                'PATCH /workouts/<id>': 'Update workout',
                'DELETE /workouts/<id>': 'Delete workout',
            },
            'exercises': {
                'GET /exercises': 'Get all exercises',
                'GET /exercises/<id>': 'Get specific exercise',
                'POST /exercises': 'Create new exercise',
                'PATCH /exercises/<id>': 'Update exercise',
                'DELETE /exercises/<id>': 'Delete exercise',
            },
            'workout_exercises': {
                'GET /workouts/<workout_id>/exercises': 'Get exercises in workout',
                'GET /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises': 'Get specific workout exercise',
                'POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises': 'Add exercise to workout',
                'PATCH /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises': 'Update exercise in workout',
            }
        }
    }, 200

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return workouts_schema.dump(Workout.query.all()), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    w = Workout.query.get(id)
    if not w: return {'error': 'Not found'}, 404
    return workout_schema.dump(w), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    if not data: return {'error': 'No data'}, 400
    new_w = Workout(**workout_schema.load(data))
    db.session.add(new_w)
    db.session.commit()
    return workout_schema.dump(new_w), 201

@app.route('/workouts/<int:id>', methods=['PATCH'])
def update_workout(id):
    w = Workout.query.get(id)
    if not w: return {'error': 'Not found'}, 404
    data = request.get_json()
    if not data: return {'error': 'No data'}, 400
    for k, v in workout_schema.load(data, partial=True).items():
        setattr(w, k, v)
    db.session.commit()
    return workout_schema.dump(w), 200

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    w = Workout.query.get(id)
    if not w: return {'error': 'Not found'}, 404
    db.session.delete(w)
    db.session.commit()
    return {'message': 'Deleted'}, 200

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return exercises_schema.dump(Exercise.query.all()), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    e = Exercise.query.get(id)
    if not e: return {'error': 'Not found'}, 404
    return exercise_schema.dump(e), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if not data: return {'error': 'No data'}, 400
    new_e = Exercise(**exercise_schema.load(data))
    db.session.add(new_e)
    db.session.commit()
    return exercise_schema.dump(new_e), 201

@app.route('/exercises/<int:id>', methods=['PATCH'])
def update_exercise(id):
    e = Exercise.query.get(id)
    if not e: return {'error': 'Not found'}, 404
    data = request.get_json()
    if not data: return {'error': 'No data'}, 400
    for k, v in exercise_schema.load(data, partial=True).items():
        setattr(e, k, v)
    db.session.commit()
    return exercise_schema.dump(e), 200

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    e = Exercise.query.get(id)
    if not e: return {'error': 'Not found'}, 404
    db.session.delete(e)
    db.session.commit()
    return {'message': 'Deleted'}, 200

@app.route('/workouts/<int:workout_id>/exercises', methods=['GET'])
def get_workout_exercises(workout_id):
    w = Workout.query.get(workout_id)
    if not w: return {'error': 'Workout not found'}, 404
    wes = WorkoutExercise.query.filter_by(workout_id=workout_id).all()
    return [workout_exercise_schema.dump(we) for we in wes], 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['GET'])
def get_workout_exercise(workout_id, exercise_id):
    we = WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first()
    if not we: return {'error': 'Not found'}, 404
    return workout_exercise_schema.dump(we), 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    if not Workout.query.get(workout_id): return {'error': 'Workout not found'}, 404
    if not Exercise.query.get(exercise_id): return {'error': 'Exercise not found'}, 404
    data = request.get_json() or {}
    data['workout_id'] = workout_id
    data['exercise_id'] = exercise_id
    new_we = WorkoutExercise(**workout_exercise_schema.load(data))
    db.session.add(new_we)
    db.session.commit()
    return workout_exercise_schema.dump(new_we), 201

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['PATCH'])
def update_workout_exercise(workout_id, exercise_id):
    we = WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first()
    if not we: return {'error': 'Not found'}, 404
    data = request.get_json()
    if not data: return {'error': 'No data'}, 400
    for k, v in workout_exercise_schema.load(data, partial=True).items():
        if k not in ['workout_id', 'exercise_id']:
            setattr(we, k, v)
    db.session.commit()
    return workout_exercise_schema.dump(we), 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)
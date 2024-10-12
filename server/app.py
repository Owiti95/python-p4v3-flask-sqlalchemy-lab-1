# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    #query the Earthquake by id
    earthquake = Earthquake.query.get(id)

    #if the earthquake with the given id exists
    if earthquake:
        #return the earthquake attributes in a JSON response
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        # if the earthquake within the given id not found, return an error message
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    #query the Earthquake model for earthquake with magnitude >= given value
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    #prepare the list of earthquakes
    quakes_list = [
        {
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
        }
        for quake in quakes
    ]

    #return json response with the count and the list of earthquakes
    return jsonify({
        "count": len(quakes_list),
        "quakes": quakes_list
    }), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)

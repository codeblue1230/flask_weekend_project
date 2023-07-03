from flask import Blueprint, request, jsonify
from game_inventory.helpers import token_required
from game_inventory.models import db, Game, game_schema, games_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return{'pass': 'test'}

# Create Game Endpoint
@api.route('/games', methods = ['POST'])
@token_required
def create_game(our_user):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    system = request.json['system']
    year_made = request.json['year_made']
    genre = request.json['genre']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    game = Game(name, description, price, system, year_made, genre, user_token)

    db.session.add(game)
    db.session.commit()

    response = game_schema.dump(game)

    return jsonify(response)

# Read 1 Game
@api.route('/games/<id>', methods = ['GET'])
@token_required
def get_game(our_user, id):
    if id:
        game = Game.query.get(id)
        response = game_schema.dump(game)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    
# Read all the Games
@api.route('/games', methods = ['GET'])
@token_required
def get_games(our_user):
    token = our_user.token
    games = Game.query.filter_by(user_token = token).all()
    response = games_schema.dump(games)
    return jsonify(response)

# Update 1 Game by ID
@api.route('/games/<id>', methods = ['PUT'])
@token_required
def update_game(our_user, id):
    game = Game.query.get(id)

    game.name = request.json['name']
    game.description = request.json['description']
    game.price = request.json['price']
    game.system = request.json['system']
    game.year_made = request.json['year_made']
    game.genre = request.json['genre']
    game.user_token = our_user.token

    db.session.commit()

    response = game_schema.dump(game)

    return jsonify(response)

# Delete 1 Game by ID
@api.route('/games/<id>', methods = ['DELETE'])
@token_required
def delete_game(our_user, id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()

    response = game_schema.dump(game)
    return jsonify(response)

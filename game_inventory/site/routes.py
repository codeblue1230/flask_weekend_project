from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from game_inventory.forms import GameForm
from game_inventory.models import Game, db


site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('landing.html')

@site.route('/profile', methods = ['GET','POST'])
@login_required
def profile():
    gameform = GameForm()

    try:
        if request.method == 'POST' and gameform.validate_on_submit():
            name = gameform.name.data
            description = gameform.description.data
            price = gameform.price.data
            system = gameform.system.data
            year_made = gameform.year_made.data
            genre = gameform.genre.data
            user_token = current_user.token

            game = Game(name, description, price, system, year_made, genre, user_token)

            db.session.add(game)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Check your form and try again.")
    
    user_token = current_user.token
    games = Game.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=gameform, games=games)
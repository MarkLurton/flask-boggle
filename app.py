from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'letsgostros'
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Home Page for Boggle Game"""
    board = boggle_game.make_board()
    session["board"] = board
    return render_template('index.html', board=board, games_played=session.get("games_played", 0), high_score=session.get("high_score", 0))

@app.route('/guess')
def handle_guess():
    """Receive guess and return result"""
    guess = request.args['guess']
    valid_check = boggle_game.check_valid_word(session['board'], guess)
    response = make_response(jsonify({ "result": f"{valid_check}"}))
    return response

@app.route('/result', methods=['POST'])
def handle_result():
    """Recieve result at end of game."""
    score = int(request.json['score'])
    saved_score = session.get('high_score', 0)
    if score > saved_score:
        session['high_score'] = score
    session["games_played"] = session.get("games_played", 0) + 1
    return f"{session['high_score']}"
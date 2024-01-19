from flask import Flask, jsonify, render_template, request, session
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()
board = boggle_game.make_board()

# Read words.txt and write to a list
with open("words.txt") as file:
  words = [word.strip() for word in file.readlines()]

@app.route("/")
def home():
    """ Display game. If playtime and score aren't already in session, instantiate them"""

    if 'playTimes' not in session:
        session['playTimes'] = 0

    if 'score' not in session:
        session['score'] = 0

    global board 
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("home.html", board=board)

@app.route('/get_score')
def get_score():
    """ When the game starts, get the score and playtime."""
    return jsonify({
        'playTimes': session['playTimes'],
        'score': session['score']
        })

@app.route("/check_word", methods=["POST"])
def check_word():
    """ Check user input against words.txt and the generated board is determine if it is valid."""
    data = request.get_json()
    word_to_check = data.get('word')

    if word_to_check in words:
        global board
        result = boggle_game.check_valid_word(board, word_to_check)
        if result == "ok":
            return jsonify({'message': 'WORKS!'})
        elif result == "not-on-board":
            return jsonify({'message': 'NOT ON BOARD'})
    else:
        return jsonify({'message': 'NOT A WORD'})

@app.route('/update_score', methods=["POST"])
def update_score():
    """ At the end of the game, update the session score and play times. If there is a new high score, update it. """
    data = request.get_json()
    score = data.get('score')
    session['playTimes'] +=1
    
    if score > session['score']:
        session['score'] = score
        return jsonify({
            'score': score,
            'playTimes': session['playTimes']
        })
    else:
        return jsonify({
            'score': session['score'],
            'playTimes': session['playTimes']
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
from crypt import methods
from unittest import result
from urllib import response
from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session
import pdb
# importing request allows the processing of incoming data
# importing jsonify allows you to turn data into JSON and wrap it in a response object
# importing session allows you to save session data on the server

app = Flask(__name__)
# this adds name as the first argument to the class Flask. name is a variable and its value depends on the Python source file it's being used in.
app.config["SECRET_KEY"] = "hereitis"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
# this is a random string used to encrypt sensitive user data like pw's

boggle_game = Boggle()

@app.route("/")
def show_homepage():
    """shows the main page"""

    board = boggle_game.make_board()
    # calls the make_board function from Boggle class to use in this instance we just created
    session['board'] = board
    # this adds board to session data
    # WHERE CAN WE SEE THIS? ANYWHERE?
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    # ARE THOSE KEYS ALREADY IN THE DICT AND WE'RE SAVING THEM TO VARIABLES, OR ARE WE CREATING THEM IN THE DICT WITH SESSION.GET

    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)
    # WHY DO WE DO BOARD=BOARD AND NOT JUST BOARD?


@app.route("/check-word")
def check_word():
    """check if word is in dictionary"""
    # SOMETHING IN BOGGLE.PY ALSO CHECKS IF A WORD IS IN THE DICT - WHY?

    word = request.args["word"]
    # pulls word from the query string
    board = session["board"]
    # pulls the current version of board from session data
    response = boggle_game.check_valid_word(board, word)
    # uses function from Boggle class to test whether word is valid and/or on the board. it returns either ok, not on board, or not word
    print (jsonify({'result': response}))
    return jsonify({'result': response})
    # converts result into JSON to send as a response

@app.route("/post-score", methods=["POST"])
def post_score():
    """takes the score, updates number of times game has been played and high score if it's been beaten"""

    score = request.json["score"]
    # WHERE IS SCORE COMING FROM? WHERE IS IT CALCULATED AND HOW DOES IT GET INTO JSON? SEEMS LIKE THE ONLY THING JSONIFY'D IS RESPONSE IN PREVIOUS FUNCTION
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    # DON'T UNDERSTAND IF THIS IS SETTING THEM TO 0 OR WHAT. WEREN'T THEY ALREADY SET BEFORE THIS?

    session['nplays'] = nplays + 1
    # adds to nplays every time this function is run
    session['highsore'] = max(score, highscore)
    # sets highscore to score or max, whichever is higher

    return jsonify(brokeRecord=score > highscore)
    
    
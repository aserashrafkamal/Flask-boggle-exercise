from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# check_word()
# update_score()

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_home(self):
        with app.test_client() as client:

            with client.session_transaction() as change_session:
                change_session['count'] = 3
                change_session['playTimes'] = 3

            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['count'], 3)
            self.assertEqual(session['playTimes'], 3)
            self.assertIn('Input a word', html)
            self.assertIn('Time remaining is 60s', html)
            self.assertIn("You've played", html)
            self.assertIn("Words:", html)

    def test_get_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['score'] = 3
                change_session['playTimes'] = 3

            res = client.get('/get_score')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['playTimes'], 3)
            self.assertEqual(session['score'], 3)

    def test_check_word(self):
        with app.test_client() as client:

            boggle_game = Boggle()
            board = boggle_game.make_board()

            result = boggle_game.check_valid_word(board, "balls")
            self.assertEqual(result, "not-word")

            result = boggle_game.check_valid_word(board, "a")
            self.assertTrue(result in ['not-on-board', 'ok'])

            result = boggle_game.check_valid_word(board, "afdgthyjkl")
            self.assertEqual(result, "not-word")

            res = client.get('/check_word')
            self.assertEqual(res.status_code, 405)

    def test_update_score(self):
        with app.test_client() as client:
            
            res = client.post('/update_score')
            self.assertEqual(res.status_code, 400)






from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    """Tests for Boggle App"""

    def test_home_page(self):
        """Test that home page renders."""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle!</h1>', html)

    def test_boggle(self):
        """Test make board function of Boggle."""
        self.assertEqual(len(Boggle.make_board(self)), 5)

    def test_guess_page(self):
        """Test receiving a guess from user"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = Boggle.make_board(self)
            res = client.get('/guess?guess=apple')

            self.assertEqual(res.status_code, 200)

    def test_results_page(self):
        """Test handling end of game"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 50
                change_session['games_played'] = 7
            
            res = client.post('/result', json={ "score" : 45 })

            with client.session_transaction() as check_session:
                self.assertEqual(res.status_code, 200)
                self.assertEqual(check_session['high_score'], 50)
                self.assertEqual(check_session['games_played'], 8)
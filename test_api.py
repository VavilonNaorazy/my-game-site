import unittest
import json
from lab1_my_api import app # импортируем наше приложение
class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        from lab1_my_api import players_db
        players_db.clear()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Добро пожаловать в мой первый API!')

    def test_get_players_empty(self):
        response = self.client.get('/players')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 0)
        self.assertEqual(data['players'], [])

    def test_add_player(self):
        new_player = {'name': 'TestPlayer', 'level': 5, 'score': 100}
        response = self.client.post('/players', data=json.dumps(new_player), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['player']['name'], 'TestPlayer')

    def test_add_player_missing_name(self):
        new_player = {'level': 5}
        response = self.client.post(
        '/players',
        data=json.dumps(new_player),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('имя', data['message'])
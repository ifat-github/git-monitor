import json
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from __init__ import app, github_webhook, PullRequest


class TestGitHubWebhook(unittest.TestCase):
    def setUp(self):
        # we should create a test DB, I didn't have enough time
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db = SQLAlchemy()
            db.init_app(app)
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db = SQLAlchemy()
            db.init_app(app)
            db.drop_all()

    def test_pull_request_valid_payload(self):
        payload = {
            'pull_request': {
                'number': 123,
                'title': 'Test Pull Request',
                'user': {
                    'login': 'test_user'
                },
                'html_url': 'https://github.com/test_user/test_repo/pull/123'
            },
            'action': 'opened'
        }
        headers = {'X-GitHub-Event': 'pull_request'}
        response = self.app.post('/github-webhook', headers=headers, data=json.dumps(payload))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'OK')

        with app.app_context():
            db = SQLAlchemy()
            db.init_app(app)
            pr = PullRequest.query.first()
            self.assertIsNotNone(pr)
            self.assertEqual(pr.number, 123)
            self.assertEqual(pr.title, 'Test Pull Request')

    def test_invalid_json_payload(self):
        headers = {'X-GitHub-Event': 'pull_request'}
        response = self.app.post('/github-webhook', headers=headers, data='invalid json payload')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), 'Bad Request: Invalid JSON payload')

    def test_missing_key_in_payload(self):
        payload = {
            'pull_request': {
                'number': 123,
                'title': 'Test Pull Request',
                'html_url': 'https://github.com/test_user/test_repo/pull/123'
            },
            'action': 'opened'
        }
        headers = {'X-GitHub-Event': 'pull_request'}
        response = self.app.post('/github-webhook', headers=headers, data=json.dumps(payload))

        self.assertEqual(response.status_code, 400)
        self.assertIn('Bad Request: Missing key', response.get_data(as_text=True))

    def test_invalid_event_type(self):
        headers = {'X-GitHub-Event': 'push'}
        response = self.app.post('/github-webhook', headers=headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), 'Not Found')


if __name__ == '__main__':
    unittest.main()

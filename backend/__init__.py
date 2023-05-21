from flask import Flask, request, jsonify, Response
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:mypassword@database-1.c0vvmasampq6.us-east-2.rds.amazonaws.com:3306/monitor'
db = SQLAlchemy(app)


class PullRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<PullRequest {self.title}>'

    def to_dict(self):
        return {'id': self.id, 'number': self.number, 'title': self.title, 'action': self.action, 'author': self.author,
                'url': self.url}


# with app.app_context():
#     db.drop_all()
#     db.create_all()


@app.route('/pullrequests')
def getPullRequests():
    try:
        pullrequests = PullRequest.query.all()
        response = [pullrequest.to_dict() for pullrequest in pullrequests]
        return jsonify(response)
    except Exception as e:
        error_message = "An error occurred while fetching pull requests."
        return jsonify({'error': error_message}), 500


@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    if request.headers.get('X-GitHub-Event') == 'pull_request':
        try:
            payload = json.loads(request.data)

            pull_request = payload['pull_request']
            pr_number = pull_request['number']
            pr_title = pull_request['title']
            action = payload['action']
            pr_author = pull_request['user']['login']
            pr_url = pull_request['html_url']

            pr = PullRequest(action=action, number=pr_number, title=pr_title, author=pr_author, url=pr_url)
            db.session.add(pr)
            db.session.commit()

            return 'OK'
        except KeyError as e:
            # Handle missing key in the payload
            return f"Bad Request: Missing key - {str(e)}", 400
        except json.JSONDecodeError:
            # Handle invalid JSON payload
            return "Bad Request: Invalid JSON payload", 400
        except Exception as e:
            # Handle other exceptions
            return f"Internal Server Error: {str(e)}", 500
    else:
        return 'Not Found', 404


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

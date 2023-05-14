from flask import Flask, request, jsonify
import json

app = Flask(__name__)


# Endpoint to receive GitHub webhook notifications
@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # Verify the request is from GitHub
    if request.headers.get('X-GitHub-Event') == 'pull_request':
        try:
            # Parse the JSON payload from GitHub
            payload = json.loads(request.data)

            # Extract the pull request details
            action = payload['action']
            pull_request = payload['pull_request']
            pr_number = pull_request['number']
            pr_title = pull_request['title']
            pr_author = pull_request['user']['login']

            # Store the pull request details in your choice of database
            # Here, we'll print them for demonstration purposes
            print(f"Action: {action}")
            print(f"PR Number: {pr_number}")
            print(f"PR Title: {pr_title}")
            print(f"PR Author: {pr_author}")

            return 'OK'
        except KeyError as e:
            # Handle missing key in the payload
            print(f"Bad Request: Missing key - {str(e)}", 400)
            return f"Bad Request: Missing key - {str(e)}", 400
        except json.JSONDecodeError:
            # Handle invalid JSON payload
            print("Bad Request: Invalid JSON payload", 400)
            return "Bad Request: Invalid JSON payload", 400
        except Exception as e:
            # Handle other exceptions
            print(f"Internal Server Error: {str(e)}", 500)
            return f"Internal Server Error: {str(e)}", 500
    else:
        print('Not Found', 404)
        return 'Not Found', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import os

import boto3
from flask import Flask, jsonify, make_response, request
from twilio.twiml.voice_response import VoiceResponse, Gather


app = Flask(__name__)


dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


USERS_TABLE = os.environ['USERS_TABLE']


@app.route('/users/<string:user_id>')
def get_user(user_id):
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    return jsonify(
        {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    )


@app.route('/users', methods=['POST'])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide both "userId" and "name"'}), 400

    dynamodb_client.put_item(
        TableName=USERS_TABLE, Item={'userId': {'S': user_id}, 'name': {'S': name}}
    )

    return jsonify({'userId': user_id, 'name': name})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.say('What follows are the meows of a cat who really wants to eat your shoelaces. Would you allow this cat to eat your shoelaces?')
            resp.play('https://shadow-penguin-3768.twil.io/assets/meowing.wav')
            resp.say('All our meowers are busy with other customers, please call again.')
            return str(resp)
        elif choice == '2':
            resp.say('What follows are the yowls of a cat who really wants to eat corn cobs but is not being allowed to because he will eat them and puke.')
            resp.say('Trigger warning for oppression and extreme deprivation.')
            resp.play('https://shadow-penguin-3768.twil.io/assets/yowling.wav')
            resp.say('Sadly this cat later jumped into the trash and tried to eat some corn cobs. We are waiting for him to puke. Goodbye.')
            return str(resp)
        elif choice == '9':
            resp.say('Sorry, out meowbox is full. Call again!')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice. If you are a cat, hang up and provide your own meowing.")

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say('Meow. Welcome to Dial A Meow services. For meowing, press 1. For yowling, press 2. To leave a meowssage, press 9.')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/answer')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

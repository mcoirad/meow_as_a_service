from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)


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

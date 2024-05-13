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
            resp.say('All our meowers are busy with other customers, please call again.')
            return str(resp)
        elif choice == '2':
            resp.say('Sorry, we have run out of yowls and waiting for delivery of more. Goodbye!')
            return str(resp)
        elif choice == '3':
            resp.say('Sorry, Rarerow is not available at this time. Goodbye!')
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.")

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say('Meow. Welcome to Dial A Meow. For Meooow, press 1. For Yowl, press 2. For Rareow, press 3.')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/answer')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

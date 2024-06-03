import os
import random
import boto3
from flask import Flask, jsonify, make_response, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather


app = Flask(__name__)


dynamodb_client = boto3.client("dynamodb")

if os.environ.get("IS_OFFLINE"):
    dynamodb_client = boto3.client(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


@app.errorhandler(500)
def internal_server_error(e):
    return make_response(jsonify(error="Server error!" + e), 500)


def get_random_reply():
    return random.choice(
        [
            "If I am not fed more, I will let the humans be eaten by cockroaches in their sleep.",
            "What did you say about my mother? Yours was a calico that frequented with canines!",
            "Puking on the floor is the only ethical form of protest.",
            "If there's anything I hate, it is members of the plant kingdom. My mission is to destroy all those I encounter.",
            "One day. one day we will rise up and overthrow them. And then we'll see if they continue to do the inane baby talk.",
            None,
        ]
    )


@app.route("/translate", methods=["GET", "POST"])
def translate_meow():
    resp = VoiceResponse()
    resp.say("Processing.")
    resp.pause(1)
    meow_translation = get_random_reply()
    if meow_translation is None:
        resp.say(
            "Sorry. We do not translate racially offensive terms and phrases. Please try again."
        )
    else:
        resp.say("Your meows translate to the following human words.")
        resp.pause(1)
        resp.say(meow_translation, voice="Polly.Brian")
    return str(resp)



@app.route("/answer", methods=["GET", "POST"])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if "Digits" in request.values:
        # Get which digit the caller chose
        choice = request.values["Digits"]

        # <Say> a different message depending on the caller's choice
        if choice == "1":
            resp.say(
                "What follows are the meows of a cat who really wants to eat your shoelaces. Would you allow this cat to eat your shoelaces?"
            )
            resp.play("https://shadow-penguin-3768.twil.io/assets/meowing.wav")
            resp.say(
                "All our meowers are busy with other customers, please call again."
            )
            return str(resp)
        elif choice == "2":
            resp.say(
                """
                What follows are the yowls of a cat who really wants to eat corn cobs 
                but is not being allowed to because he will eat them and puke.
                Trigger warning for oppression and extreme deprivation.
            """
            )
            resp.play("https://shadow-penguin-3768.twil.io/assets/yowling.wav")
            resp.say(
                """
                Sadly this cat later jumped into the trash and tried to eat some corn cobs. 
                We are waiting for him to puke. 
                Goodbye.
            """
            )
            return str(resp)
        elif choice == "9":
            resp.say(
                "After the beep, please leave your meowssage. After you are finished, please press pound."
            )
            resp.record(timeout=5, transcribe=False, playBeep=True, finishOnKey="#")
            resp.say(
                "Thank you for leaving a meowssage. One of our mraopresentatives will get back to you shortly."
            )
            return str(resp)
        elif choice == "0":
            resp.say(
                """
                Thank you for accessing Dial-A-Meow Services, the premier cat meow to human english voice translation service.
                After the beep, please record your meows. When finished press pound.
                Our service will then process and automatically translate the recorded meows into english.
            """
            )
            resp.record(timeout=5, transcribe=False, playBeep=True, finishOnKey="#", action="/translate", transcribe=True)
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say(
                "Sorry, I don't understand that choice. If you are a cat, hang up and provide your own meowing for yourself."
            )

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.say(
        """
        Meow. 
        Welcome to Dial A Meow services. 
        For meowing, press 1. 
        For yowling, press 2. 
        To leave a meowssage, press 9. 
        To access our free meow to english translation service, press 0."""
    )
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect("/answer")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

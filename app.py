from flask import Flask, Response
from twilio.twiml.voice_response import Dial, VoiceResponse
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

from_number = os.environ["TWILIO_NUMBER"]
to_number = os.environ["DESTINATION_NUMBER"]


@app.route("/twiml", methods=["GET", "POST"])
def twiml_route():
    twiml = VoiceResponse()
    dial = Dial(caller_id=from_number)
    dial.number(to_number)
    twiml.append(dial)
    return Response(str(twiml), mimetype="text/xml")


if __name__ == "__main__":
    app.run()

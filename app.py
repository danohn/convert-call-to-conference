from flask import Flask, Response, request
from twilio.twiml.voice_response import Dial, VoiceResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

from_number = os.environ["TWILIO_NUMBER"]
to_number = os.environ["DESTINATION_NUMBER"]


@app.route("/twiml", methods=["POST"])
def twiml_route():
    twiml = VoiceResponse()
    dial = Dial(caller_id=from_number, answer_on_bridge=True, action="/convert")
    dial.number(
        to_number,
        status_callback="/number-status-callback",
        status_callback_event="initiated ringing answered completed",
        status_callback_method="POST",
    )
    twiml.append(dial)
    return Response(str(twiml), mimetype="text/xml")


@app.route("/convert", methods=["POST"])
def convert_route():
    parent_call_sid = request.form.get("ParentCallSid")
    call_sid = request.form.get("CallSid")

    twiml = VoiceResponse()
    dial = Dial()

    # checks if a call is a parent or child
    # (by checking the existence of the ParentCallSid parameter)
    if parent_call_sid:
        dial.conference(
            name=parent_call_sid,
            beep=False,
            start_conference_on_enter=True,
            end_conference_on_exit=True,
            jitter_buffer_size="off",
            status_callback="/conference-status-callback",
            status_callback_event="start end join leave",
            status_callback_method="POST",
        )
        twiml.append(dial)
        return Response(str(twiml), mimetype="text/xml")
    else:
        dial.conference(
            name=call_sid,
            beep=False,
            start_conference_on_enter=True,
            end_conference_on_exit=True,
            jitter_buffer_size="off",
            status_callback="/conference-status-callback",
            status_callback_event="start end join leave",
            status_callback_method="POST",
        )
        twiml.append(dial)
        return Response(str(twiml), mimetype="text/xml")


@app.route("/number-status-callback", methods=["POST"])
def number_status_calback_route():
    return Response(status=204)


@app.route("/conference-status-callback", methods=["POST"])
def conference_status_calback_route():
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)

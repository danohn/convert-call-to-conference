# Convert call to conference

A Python implementation of converting a Twilio bridged call to a conference call

## Background

When using Twilio, a bridged call occurs when an incoming call leg (also known as the parent call) gets instructions (via TwiML) to `<Dial>` a `<Number>`, `<Client>` or `<Sip>` leg. This then creates the outgoing call leg (also known as the child call). In order to convert this bridged call to a conference call (to for example use attended/blind transfer or agent coaching), it is necessary to first update the child call with new TwiML instructions to `<Dial>` a `<Conference>`. This will then cause the parent call to get new TwiML instructions from it's `action` URL (if it exists). If the `action` URL returns TwiML to `<Dial>` the same conference, both parties will be able to continue talking.

## Installation

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env`
5. `nano .env` (replace placeholders with real values)

## Usage

Once the virtual environment has been activated, start the Flask app by running `python app.py`. You will also need to start an Ngrok session by running `ngrok http 5000` if your host does not have a public IP or has a NAT port forward from the internet firewall.

Once started, update the Twilio phone number, SIP Domain or TwiML App to the Ngrok URL or public IP/hostname. When a call comes in to Twilio, the Flask app will return standard TwiML to `<Dial>` the `<Number>` from the `.env` file. This will be a regular bridged call. To convert the bridged call to a conference, run `python convert.py`. The conversion script makes the assumption that there is only 1 active bridged call (with 2 call legs/SIDs) and as such, converts the latest call (the child call) to `<Dial>` a `<Conference>`. The conference name will be the parent Call SID (since SIDs are unique). The `action` URL will also return TwiML instructions to the parent call to join the same conference.

`<Number>` and `<Conference>` status callbacks have also been implemented for debugging purposes.

## Real world implementation

As previously mentioned, this script is designed to run in a dev/lab environment where only 1 call at a time takes place. This is due to the conversion script simply updating the latest call from the `/Calls` REST API. In a production environment, the conversion initiation could take place from a Web UI that targets a specific Call SID/child call.

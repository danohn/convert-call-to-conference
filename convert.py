from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

base_url = os.environ["NGROK_URL"]

calls = client.calls.list(status="in-progress")

# calls[0] will always be the latest Call SID (child call).
# To convert a call from a bridged call to a conference, we need
# to first target the child call. This will cause the parent call
# to reach out to the action URL which should connect to the same conference

target_sid = calls[0].sid

call_to_update = client.calls(target_sid).update(
    method="POST", url=f"{base_url}/convert"
)

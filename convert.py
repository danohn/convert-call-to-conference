from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

calls = client.calls.list(status='in-progress')

#calls[0] will always be the latest Call SID. Since we want to target the inbound Call SID, we need to get the 2nd latest entry
target_sid = calls[1].sid

from twilio.rest import Client
from credentials import account_sid, auth_token, my_phone, my_twilio


client = Client(account_sid, auth_token)

my_msg = 'Testing Credentials.py'
def send_sms():
	return client.messages.create(
                            to=contactNum,
                            from_=my_twilio,
                            body=message)
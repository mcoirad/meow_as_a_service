# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC2b66693878f1718d85c12ff39f54e372'
auth_token = 'aa3c105719f26af587b331f07ad25868'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+17033417667',
                        from_='+13373835033'
                    )

print(call.sid)

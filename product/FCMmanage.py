from firebase_admin import credentials, messaging
import firebase_admin
from Shopx.settings import BASE_DIR
import os


file = os.path.join(BASE_DIR, 'firstproject-daf7e-firebase-adminsdk-rr9oq-84b213bc75.json')
cred = credentials.Certificate(file)
firebase_admin.initialize_app(cred)

def sendPush(title,registration_token,msg):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title,
                                            body=msg),
    tokens=registration_token

    )

    response = messaging.send_multicast(message)
    print(f"The message has successfully send {response}")

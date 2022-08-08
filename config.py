import os
import base64

privateKey = str(base64.b64decode(os.environ.get("PRIVATE_KEY")).decode("utf-8", "ignore"))
# print(privateKey)
firebase_config = {
  "type": "service_account",
  "project_id": "mcoord-bot",
  "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
  "private_key": privateKey,
  "client_email": "firebase-adminsdk-39inc@mcoord-bot.iam.gserviceaccount.com",
  "client_id": "108849099594782041510",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-39inc%40mcoord-bot.iam.gserviceaccount.com"
}

databaseUrl = os.environ.get("DATABASE_URL")
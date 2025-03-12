#!./.venv/bin/python3
import os
import sys
import time
import json
import base64
import google.auth
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow
from email.mime.text import MIMEText
from datetime import datetime, timezone
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Grant access to Google's APIs
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.courses.readonly"
]

# Address to send notifications from
SENDER_ADDRESS = os.environ.get("PJNOTIFIER_SENDER_ADDRESS")
if SENDER_ADDRESS is None:
    print("Please provide a sender email address using the PJNOTIFIER_SENDER_ADDRESS environment variable.")
    exit(1)


# List of notification receivers
RECIPIENTS = [SENDER_ADDRESS]

# Credentials to authenticate to Google
creds = None

if os.path.isfile("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0, login_hint=SENDER_ADDRESS, access_type="offline", prompt="consent", include_granted_scopes="true")
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

if len(sys.argv) > 1 and sys.argv[1] == "auth":
    exit(0)

# IDs of the classroom, material
FYZIKA_SEXTA_ID = "710065885050"
PJUV_MATROS_ID = "711599395395"
PJUV_MATROS_URL = "https://classroom.google.com/c/NzEwMDY1ODg1MDUw/m/NzExNTk5Mzk1Mzk1/details"

# Service discovery
classroom = build("classroom", "v1", credentials=creds)
gmail = build("gmail", "v1", credentials=creds)

courses = classroom.courses()
materials = courses.courseWorkMaterials()

pjuv_matros = materials.get(courseId=FYZIKA_SEXTA_ID, id=PJUV_MATROS_ID).execute()

update_time = pjuv_matros["updateTime"]
prev_update_time = None

try:
    with open("prev_update_time.txt", "r+") as f:
        prev_update_time = f.read().removesuffix("\n")
        f.seek(0)
        f.truncate(0)
        f.write(update_time + "\n")
except IOError:
    with open("prev_update_time.txt", "w+") as f:
        f.write(update_time + "\n")

print("Last update time:")
print(f"  previous: {prev_update_time}")
print(f"  current:  {update_time}")

# Dictionary[id -> (name, type)]
materialy = {}
materialy_str = ""
for mat in pjuv_matros["materials"]:
    match mat:
        case {"driveFile":{"driveFile":{"id": file_id, "title": title, "alternateLink": alternateLink, "thumbnailUrl": thumbnailUrl}, "shareMode": shareMode}}:
            materialy[file_id] = (title, "soubor")
        case {"form":{"formUrl": formUrl, "responseUrl": responseUrl, "thumbnailUrl": thumbnailUrl, "title": title}}:
            materialy[formUrl] = (title, "formulář google")
        case {"link":{"url": url, "thumbnailUrl": thumbnailUrl, "title": title}}:
            materialy[url] = (title, "odkaz")
        case {"youtubeVideo":{"id": video_id, "alternateUrl": alternateUrl, "thumbnailUrl": thumbnailUrl, "title": title}}:
            materialy[video_id] = (title, "youtube video")
        case _:
            print("unknown material")

prev_materialy = None
try:
    with open("prev_materialy.json", "r+") as f:
        prev_materialy = json.load(f)
        f.seek(0)
        f.truncate(0)
        json.dump(materialy, f)
except IOError:
    with open("prev_materialy.json", "w+") as f:
        json.dump(materialy, f)

prev_materialy_set = set(prev_materialy)
materialy_set = set(materialy)

deleted = list(map(lambda x: prev_materialy[x], prev_materialy_set - materialy_set))
added = list(map(lambda x: materialy[x], materialy_set - prev_materialy_set))

print("Materials:")
print(f"  added: {added}")
print(f"  deleted: {deleted}")

for (title, typ) in deleted:
    materialy_str += f"<samp class=\"red change\"><b>---</b> {typ}: {title}</samp>\n"

for (title, typ) in added:
    materialy_str += f"<samp class=\"green change\"><b>+++</b> {typ}: {title}</samp>\n"

#dbg_send_email = True
dbg_send_email = False

# Date in local time
dt = datetime.fromisoformat(update_time).astimezone(datetime.now().astimezone().tzinfo)
time_str = dt.strftime("%-d. %-m. %Y  %-H:%M:%S")

if update_time != prev_update_time or dbg_send_email:
    html = f"""
           <html>
               <head>
               <style>
               .green \u007b
                   color: rgb(34, 139, 34);
               \u007d
               .red \u007b
                   color: rgb(178, 34, 34);
               \u007d
               .change \u007b
                   display: block;
                   margin-bottom: 0.25rem;
               \u007d
               </style>
               </head>
               <body>
                   <h1>PJ Classroom Notifier 1.0</h1>
                   <a href="{PJUV_MATROS_URL}">Odkaz na materiál v učebně</a>
                   <p>Čas poslední úpravy: <b>{time_str}</b></p>
                   <h2 style="margin-bottom: 0.25rem;">Změny:</h2>
                   <div style="font-size: 1rem; margin-left: 0.25rem;">
                   {materialy_str}
                   </div>
               </body>
           </html>
           """
    message = MIMEText(html, "html")
    message["To"] = ", ".join(RECIPIENTS)
    message["From"] = SENDER_ADDRESS
    message["Subject"] = "PJ upravil materiál!"

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": encoded_message}
    sent_message = (
        gmail.users()
        .messages()
        .send(userId="me", body=body)
        .execute()
    )

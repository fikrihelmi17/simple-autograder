import os
import json
from utils import unhandled_exception

def generate_report(checklist, report_path, username):
    report = create_report(checklist)
    report["Message"] = generate_templated_message(report, username)
    save(report, report_path)

def generate_templated_message(report, username):
    if is_submission_approved(report):
        return "Selamat <b>" + username + "!!</b> kamu telah lolos submission ini."

    message = ""
    for item in report["ChecklistsCompleted"]:
        message += "<li>" + item + "</li>"
    return "Hallo " + username + " masih terdapat beberapa kesalahan, berikut adalah kesalahan yang terjadi <ul>" + message + "</ul>. Silakan diperbaiki yaa."

def is_submission_approved(report):
    return len(report["ChecklistsCompleted"]) == 6

def create_report(checklists):
    messages = []
    checklist_completed = []

    for key, value in checklists.__dict__.items():
        message = value.comment
        if message != "":
            messages.append("<li>" + message + "</li>")

        if value.status:
            checklist_completed.append(key)

    return {
        "ChecklistsCompleted": checklist_completed,
        "Message": "".join(messages)
    }

def save(report, report_path):
    try:
        with open(os.path.join(report_path, "report.json"), 'w') as file:
            json.dump(report, file, indent=4)
    except Exception as e:
        unhandled_exception(e)
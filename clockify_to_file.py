import requests
import json
from datetime import datetime

CLOCKIFY_API_KEY = "NmM2MTY1MGMtYjkzYS00MGVkLWE1MTAtOTJkZmJkYmNkYzky"
WORKSPACE_ID = "656417f73f3a0765771afe83"
USER_ID = "656417f73f3a0765771afe80"

def get_all_activities():
    url = f'https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries'
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": CLOCKIFY_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching time activities. Status code: {response.status_code}")
        return None

def get_subject_name(project_id):
    url = f'https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects/{project_id}'
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": CLOCKIFY_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def format_utc(utc):
    duration_str = utc[2:]

    if duration_str == "0S":
        return "0h, 0m"

    hours, minutes = 0, 0
    if 'H' in duration_str:
        hours = duration_str.split("H")[0]
    if 'M' in duration_str:
        minutes = duration_str.split("H")[-1].split("M")[0]

    return f"{hours}h, {minutes}m"

activities = get_all_activities()
if activities:
    activities_data = []
    for entry in activities:
        if not entry['timeInterval']['end']:
            project = get_subject_name(entry['projectId'])
            description = entry['description'] if entry['description'] else "No Description Provided"
            utc = entry['timeInterval']['start']
            utc_timestamp = datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
            epoch = int((utc_timestamp - datetime(1970, 1, 1)).total_seconds())
            state = f"{project['name']}" if project else "No Subject Provided"
            project_duration = format_utc(project['duration']) if project else "0h, 0m"
            activities_data.append({
                "description": description,
                "state": state,
                "project_duration": project_duration,
                "epoch": epoch
            })
    with open('activities.json', 'w') as json_file:
        json.dump(activities_data, json_file)
else:
    print("Unable to fetch time activities.")

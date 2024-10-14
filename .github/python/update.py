import requests
import json
import os

token = os.environ["TOKEN"]
params = {
  "api_key": token,
  "offset": "0",
  "limit": "20",
  "include_options": "1"
}
r = requests.get('https://www.parsehub.com/api/v2/projects', params=params)
data=json.loads(r.text)
#print(data["total_projects"])
proj_num=(data["total_projects"]) #numero progetti
i = 0
while i < proj_num:
    title = data["projects"][i]["title"]
    project_token = data["projects"][i]["token"]
    latest_run = None
    
    # Verifica se "last_ready_run" non è None
    if data["projects"][i]["last_ready_run"] is not None:
        latest_run = data["projects"][i]["last_ready_run"]["run_token"]
    
    # Procedi solo se latest_run non è None
    if latest_run is not None:
        run_token_string = "https://www.parsehub.com/api/v2/runs/" + latest_run + "/data"
        j = requests.get(run_token_string, params=params)
        json_file = json.loads(j.text)
        
        # Salva il file JSON
        file_name = title + ".json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)
    
    i += 1


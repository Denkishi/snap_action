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
data = json.loads(r.text)

# Verifica se la chiave "total_projects" esiste
proj_num = data.get("total_projects", 0)  # Imposta a 0 se non esiste

i = 0
while i < proj_num:
    title = data["projects"][i]["title"]
    project_token = data["projects"][i]["token"]
    
    # Controlla se "last_ready_run" non è None
    last_ready_run = data["projects"][i].get("last_ready_run")
    if last_ready_run is not None:
        latest_run = last_ready_run.get("run_token")
        if latest_run:
            run_token_string = f"https://www.parsehub.com/api/v2/runs/{latest_run}/data"
            j = requests.get(run_token_string, params=params)
            json_file = json.loads(j.text)
            
            file_name = f"{title}.json"
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(json_file, f, ensure_ascii=False, indent=4)
    else:
        print(f"Nessuna esecuzione disponibile per il progetto: {title}")
    
    i += 1


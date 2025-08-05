import os
import requests
import time
import base64

human_dataset = "dataset/html/human/"
os.makedirs(human_dataset, exist_ok=True)


keywords = [
    "todo list",
    "weather app",
    "newsletter signup",
    "contact form",
    "snake game",
    "game",
    "business page",
    "calendar widget"
    'feedback form'
    'survey form'
    'event registration'
    'donation form'
    'appointment scheduler'
    'ticket booking'
    "reservation system"
    "invoice template"
    "pomodoro timer"
]


#max amount of files per keyword
files_keyword = 75

gh_url = "https://api.github.com/search/code" 

token = os.environ.get("GITHUB_TOKEN")

if token:
    headers = {
        "accept": "application/vnd.github.v3.text-match+json",
        "Authorization": f"token {token}",
        "User-Agent": "divpreet"
    }

else:
    headers = {
        "accept": "application/vnd.github.v3.text-match+json",
    }

def raw(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json = response.json()
    content = json.get('content')
    encoding = json.get('encoding')
    if encoding == "base64":
        code = base64.b64decode(content).decode("utf-8")
    else:
        code = content
    
    return code

count = 0
for w in keywords:
    time.sleep(2.5)
    params = {
        "q": f"{w} in:file language:html extension:html",
        "per_page": files_keyword
    }
    print(w)
    response = requests.get(gh_url, headers=headers, params=params)
    response.raise_for_status()
    output = response.json().get('items', [])

    for i in output:
        path = i["path"]        
        if not path.endswith(".html"):
            continue

        # using api endpoint instead of raw url method
        api_url = i["url"]
        try:
            code = raw(api_url)

        except Exception as e:
            print(e)
            continue

        count += 1
        file = f"{count}.html"
        path = os.path.join(human_dataset, file)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(path)

print("done")




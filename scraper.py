import os
import requests

human_dataset = "dataset/human"

keywords = [
    "sort list",
    "fibbonaci",
    "to do list",
    "command line",
    "web server",
    "csv reader",
    "flask server",
    "tkinter",
    "command line",
    "numpy",
    "pygame",
    "pil images",
    "beautiful soup",
    "requests",
    "argparse"
]


#max amount of files per keyword
files_keyword = 75

gh_url = "https://api.github.com/search/code" 

token = os.environ.get("GITHUB_TOKEN")

if token:
    headers = {
        "accept": "application/vnd.github.v3.text-match+json",
        "Authorization": f"token {token}"
    }

else:
    headers = {
        "accept": "application/vnd.github.v3.text-match+json",
    }

def raw(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

count = 0
for w in keywords:
    params = {
        "q": f"{w} in:file language:python extension:py",
        "per_page": files_keyword
    }
    print(w)
    response = requests.get(gh_url, headers=headers, params=params)
    response.raise_for_status()
    output = response.json().get('items', [])

    for i in output:
        # raw path
        repo = i["repository"]
        name = repo["full_name"]
        branch = repo.get("default_branch", "main")
        path = i["path"]
        
        if not path.endswith(".py"):
            continue

        raw_url = f"https://raw.githubusercontent.com/{repo['full_name']}/{branch}/{path}"
        
        try:
            code = raw(raw_url)
        
        except Exception as e:
            print(e)
            continue

        count += 1
        file = f"{count}.py"
        path = os.path.join(human_dataset, file)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print(path)

print("done")




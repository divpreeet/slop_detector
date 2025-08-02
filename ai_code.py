import os
import requests
import time
import re


os.makedirs('dataset/ai', exist_ok=True)


prompts = [
    "write a to-do list in python",
    "generate a calculator in python",
    "generate a weather viewer in python",
    "write a python script about the fibonacci sequence",
    "write a python script that checks if a number is prime",
    "write a simple image viewer in python",
    "write a python script that converts html to markdown",
    "make a simple image viewer in python using tkinter",
    "write a system monitor in python",
    "wrtie python code to sort fileas in folders ",
    "generate code for a python project that scales images to 1920x1080",
    "write a discord bot in python that gets a random repo from github",
    "generate a portfolio in a terminal in python",
    "generate a terminal based clock app in python",
    "make a task manager in python",
    "make a adventure rpg terminal based game in python",
    "make a rock paper scissors game in python using tkinter",
    "make a web scraper made in python",
    "generate a word sorter in python",
    "make a random country name generator in python",
]

api = "https://ai.hackclub.com/chat/completions"

def get_code(code):
    m = re.search(r"```(?:python)?\n(.+?)```", code, flags=re.S)
    if m:
        return m.group(1).strip()
    return code.strip()

for ind, prompt in enumerate(prompts, start=1):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a code generator, provide ONLY the final PYTHON code, dont provide any explanations, or notes. provide comments in the code explaining it."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        output = requests.post(api, json=payload)
        output.raise_for_status()
        raw = output.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        continue
    
    code = get_code(raw)

    path = f"dataset/ai/a{ind}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write(code + "\n")

    print(path)
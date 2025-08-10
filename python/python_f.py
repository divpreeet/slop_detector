#python feature extraction
import os
import csv
import ast
import re

root = os.path.dirname(os.path.dirname(__file__)) 

ai_dataset = os.path.join(root, 'dataset', 'python', 'ai')
human_dataset = os.path.join(root, 'dataset', 'python', 'human')
csv_path = os.path.join(root, 'dataset', 'python.csv')

def features(code):
    lines = code.splitlines()
    num_l = len(lines)
    num_b = sum(1 for l in lines if not l.strip())
    comment_r = sum(1 for l in lines if l.strip().startswith('#')) / max(num_l, 1)
    avg_l_len = sum(len(l) for l in lines) / max(num_l, 1)
    indents = set()
    for l in lines:
        match = re.match(r'^(\s+)', l)
        if match:
            indents.add(match.group(1))

    indent_var = len(indents)

    try:
        tree = ast.parse(code)
        num_funcs = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))
    except SyntaxError:
        num_funcs = 0

    return {
        'lines': num_l,
        'blanks': num_b,
        'comment ratio': comment_r,
        'line length': avg_l_len,
        'indent variations': indent_var,
        'functions': num_funcs,
        "code": code
    }

if not os.path.isdir(human_dataset):
    raise FileNotFoundError(human_dataset)

fieldnames = ['filename', 'label'] + list(features("").keys())

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for label, folder in [('ai', ai_dataset), ('human', human_dataset)]:
        for file in sorted(os.listdir(folder)):
            if not file.endswith(".py"):
                continue
            
            path = os.path.join(folder, file)
            with open(path, encoding='utf-8') as f:
                code = f.read()
            feats = features(code)
            row = {"filename": file, "label": label, ** feats}
            writer.writerow(row)
            print(file)
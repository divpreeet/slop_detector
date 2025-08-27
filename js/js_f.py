#js feature extraction

import os
import csv

import re

root = os.path.dirname(os.path.dirname(__file__)) 

ai_dataset = os.path.join(root, 'dataset', 'js', 'ai')
human_dataset = os.path.join(root, 'dataset', 'js', 'human')
csv_path = os.path.join(root, 'dataset', 'js.csv')

def features(code):
    lines = code.splitlines()
    num_l = len(lines)
    num_b = sum(1 for l in lines if not l.strip())

    # no of lines that are comments
    comment_l = 0
    for i in lines:
        strip = i.strip()
        if strip.startswith('//'):
            comment_l += 1
        if strip.startswith('/*'):
            comment_l += 1
        if strip.startswith('*'):
            comment_l += 1
        if strip.startswith('*/'):
            comment_l += 1
    comment_r = comment_l / max(num_l, 1)
    avg_l_len = sum(len(l) for l in lines) / max(num_l, 1)
    indents = set()
    for l in lines:
        match = re.match(r'^(\s+)', l)
        if match:
            indents.add(match.group(1))

    indent_var = len(indents)
    
    num_funcs = len(re.findall(r'\bfunction\b', code)) + len(re.findall(r'=>', code))
    
    num_arrows = len(re.findall(r'=>', code))
    arrow_r = num_arrows / max(num_funcs + num_arrows, 1)
    vars_funcs =  re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', code)
    avg_ind_len = sum(len(n) for n in vars_funcs) / max(len(vars_funcs), 1)

    return {
        'lines': num_l,
        'blanks': num_b,
        'comment ratio': comment_r,
        'line length': avg_l_len,
        'indent variations': indent_var,
        'functions': num_funcs + num_arrows,
        'arrow ratio': arrow_r,
        'avg ind len': avg_ind_len,
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
            if not file.endswith(".js"):
                continue
            
            path = os.path.join(folder, file)
            with open(path, encoding='utf-8') as f:
                code = f.read()
            feats = features(code)
            row = {"filename": file, "label": label, ** feats}
            writer.writerow(row)
            print(file)
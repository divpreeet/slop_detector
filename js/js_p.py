# js prediction

import sys
import pandas as pd
import joblib
import re

# reusing code from features
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


file_path = sys.argv[1]
with open(file_path, encoding='utf-8') as f:
    code = f.read()

features = features(code)
renamed = {
    'num_l': features['lines'],
    'num_b': features['blanks'],
    'comment_r': features['comment ratio'],
    'avg_l_len': features['line length'],
    'indent_var': features['indent variations'],
    'num_funcs': features['functions'],
    'arrow_r': features['arrow ratio'],
    'avg_ind_len': features['avg ind len'],
    'code': features['code'],
}

cols = ['num_l', 'num_b', 'comment_r', 'avg_l_len', 'indent_var', 'num_funcs', 'arrow_r', 'avg_ind_len', 'code']
df = pd.DataFrame([renamed], columns=cols)

pipeline = joblib.load('models/js.pkl')
prediction = pipeline.predict(df)[0]
prob = pipeline.predict_proba(df)[0]

if prediction == 1:
    label = "AI"
    confidence = prob[1] * 100
else: 
    label = "human"
    confidence = prob[0] * 100

print(f"{file_path} is {confidence:.2f}% likely to be {label}")
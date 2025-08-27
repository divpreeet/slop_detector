# python prediction

import sys
import pandas as pd
import joblib
import ast
import re

# reusing code from features
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
    'code': features['code'],
}

df = pd.DataFrame([renamed])

pipeline = joblib.load('models/python.pkl')
prediction = pipeline.predict(df)[0]
prob = pipeline.predict_proba(df)[0]

if prediction == 1:
    label = "AI"
    confidence = prob[1] * 100
else: 
    label = "human"
    confidence = prob[0] * 100

print(f"{file_path} is {confidence:.2f}% likely to be {label}")
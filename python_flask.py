# flask python functon

import pandas as pd
import joblib
import re
import os
import ast

# im tired of writing comments 
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

def python(code):
    features_dict = features(code)
    renamed = {
        'num_l': features_dict['lines'],
        'num_b': features_dict['blanks'],
        'comment_r': features_dict['comment ratio'],
        'avg_l_len': features_dict['line length'],
        'indent_var': features_dict['indent variations'],
        'num_funcs': features_dict['functions'],
        'code': features_dict['code'],
    
    }

    cols = ['num_l', 'num_b', 'comment_r', 'avg_l_len', 'indent_var', 'num_funcs', 'code']
    
    df = pd.DataFrame([renamed], columns=cols)

    model_path = os.path.join(os.path.dirname(__file__), "models", 'python.pkl')

    pipeline = joblib.load(model_path)
    prediction = pipeline.predict(df)[0]
    prob = pipeline.predict_proba(df)[0]

    if prediction == 1:
        label = "AI"
        confidence = prob[1] * 100
    else:
        label = "human"
        confidence = prob[0] * 100

    return f"{confidence:.2f}% likely to be {label}"
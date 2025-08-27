#flask function

import pandas as pd
import joblib
import re
import os

# reusing code from js 
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

def javascript(code):
    features_dict = features(code)
    renamed = {
        'num_l': features_dict['lines'],
        'num_b': features_dict['blanks'],
        'comment_r': features_dict['comment ratio'],
        'avg_l_len': features_dict['line length'],
        'indent_var': features_dict['indent variations'],
        'num_funcs': features_dict['functions'],
        'arrow_r': features_dict['arrow ratio'],
        'avg_ind_len': features_dict['avg ind len'],
        'code': features_dict['code'],
    }

    cols = ['num_l', 'num_b', 'comment_r', 'avg_l_len', 'indent_var', 'num_funcs', 'arrow_r', 'avg_ind_len', 'code']
    df = pd.DataFrame([renamed], columns=cols)

    model = os.path.join(os.path.dirname(__file__), "models", 'js.pkl')
    pipeline = joblib.load(model)
    prediction = pipeline.predict(df)[0]
    prob = pipeline.predict_proba(df)[0]


    if prediction == 1:
        label = "AI"
        confidence = prob[1] * 100
    else: 
        label = "human"
        confidence = prob[0] * 100
    
    return f"{confidence:.2f}% likely to be {label}"
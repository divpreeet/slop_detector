#flask function

import pandas as pd
import joblib
import re
import os

# reusing code from ts
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

    # functions
    func_pattern = r'\bfunction\b|\basync\b\s*(function)?|\b\w+\s*\([^)]*\)\s*:\s*\w+\s*{|=>'

    num_funcs = len(re.findall(func_pattern,code))
    num_arrows = len(re.findall(r'=>', code))
    arrow_r = num_arrows / max(num_funcs + num_arrows, 1)
    vars_funcs =  re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', code)
    avg_ind_len = sum(len(n) for n in vars_funcs) / max(len(vars_funcs), 1)

    num_interfaces = len(re.findall(r'\binterface\b', code))
    num_types = len(re.findall(r'\btype\b', code))
    num_enums = len(re.findall(r'\benum\b', code))
    num_classes = len(re.findall(r'\bclass\b', code))
    num_imports = len(re.findall(r'\bimport\b', code))
    num_exports = len(re.findall(r'\bexport\b', code))
    type_annotations = len(re.findall(r':\s*[A-Za-z_][A-Za-z0-9_<>,\[\]\s]*', code))
    generics = len(re.findall(r'<[A-Za-z_][A-Za-z0-9_,\s]*>', code))

    access_mods = len(re.findall(r'\b(public|private|protected|readonly)\b', code))

    vars_funcs = re.findall(r'\b([A-Za-z_][A-Za-z0-9_]*)\b', code)

    return {
        'lines': num_l,
        'blanks': num_b,
        'comment ratio': comment_r,
        'line length': avg_l_len,
        'indent variations': indent_var,
        'functions': num_funcs + num_arrows,
        'arrow ratio': arrow_r,
        'avg ind len': avg_ind_len,
        "code": code,
        'interfaces': num_interfaces,
        'types': num_types,
        'enums': num_enums,
        'classes': num_classes,
        'imports': num_imports,
        'exports': num_exports,
        'type annotations': type_annotations,
        'generics': generics,
        'access modifiers': access_mods
    }

def typescript(code):
    f = features(code)
    renamed = {
        'num_l': f['lines'],
        'num_b': f['blanks'],
        'comment_r': f['comment ratio'],
        'avg_l_len': f['line length'],
        'indent_var': f['indent variations'],
        'num_funcs': f['functions'],
        'arrow_r': f['arrow ratio'],
        'num_interfaces': f['interfaces'],
        'num_types': f['types'],
        'num_enums': f['enums'],
        'num_classes': f['classes'],
        'num_imports': f['imports'],
        'num_exports': f['exports'],
        'type_annotations': f['type annotations'],
        'generics': f['generics'],
        'access_mods': f['access modifiers'],
        'avg_ind_len': f['avg ind len'],
        'code': f['code'],
    }

    cols = [
        'num_l', 'num_b', 'comment_r', 'avg_l_len', 'indent_var', 'num_funcs', 'arrow_r',
        'num_interfaces', 'num_types', 'num_enums', 'num_classes', 'num_imports', 'num_exports',
        'type_annotations', 'generics', 'access_mods', 'avg_ind_len', 'code'
    ]
    df = pd.DataFrame([renamed], columns=cols)

    pipeline = joblib.load('models/ts.pkl')
    prediction = pipeline.predict(df)[0]
    prob = pipeline.predict_proba(df)[0]


    if prediction == 1:
        label = "AI"
        confidence = prob[1] * 100
    else: 
        label = "human"
        confidence = prob[0] * 100
    
    return f"{confidence:.2f}% likely to be {label}"
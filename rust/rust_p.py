# rust prediction

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
        if strip.startswith("///"):
            comment_l += 1
        if strip.startswith("/*"):
            comment_l += 1
        if strip.startswith("/*!"):
            comment_l += 1
        if strip.startswith("*"):
            comment_l += 1
        if strip.startswith("*/"):
            comment_l += 1

    comment_r = comment_l / max(num_l, 1)
    avg_l_len = sum(len(l) for l in lines) / max(num_l, 1)
    indents = set()
    for l in lines:
        match = re.match(r"^(\s+)", l)
        if match:
            indents.add(match.group(1))

    indent_var = len(indents)

    num_funcs = len(re.findall(r"\bfn\b", code))
    num_structs = len(re.findall(r"\bstruct\b", code))
    vars_funcs = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", code)

    num_enums = len(re.findall(r"\benum\b", code))
    num_traits = len(re.findall(r"\btrait\b", code))
    num_impls = len(re.findall(r"\bimpl\b", code))
    num_mods = len(re.findall(r"\bmod\b", code))
    num_use = len(re.findall(r"\buse\b", code))
    num_pub = len(re.findall(r"\bpub\b", code))
    num_const = len(re.findall(r"\bconst\b", code))
    num_macro = len(re.findall(r"\w+!", code))
    num_tests = len(re.findall(r"#\[test\]", code))
    generics = len(re.findall(r"<[A-Za-z_][A-Za-z0-9_,\s]*>", code))
    num_lifetimes = len(re.findall(r"'\w+", code))
    num_match = len(re.findall(r"\bmatch\b", code))
    unsafe = len(re.findall(r"\bunsafe\b", code))
    if_let = len(re.findall(r"\bif let\b", code))
    num_if = len(re.findall(r"\bif\b", code))
    num_while = len(re.findall(r"\bwhile\b", code))
    num_loop = len(re.findall(r"\bloop\b", code))
    num_questions = code.count("?")
    num_todo = len(re.findall(r"TODO", code))
    doc_comms = sum(
        1 for l in lines if l.strip().startswith("///") or l.strip().startswith("//!")
    )

    vars_funcs = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", code)
    avg_ind_len = sum(len(n) for n in vars_funcs) / max(len(vars_funcs), 1)

    type_annotations = len(re.findall(r":\s*[A-Za-z_][A-Za-z0-9_<>,\[\]\s]*", code))

    cond_total = num_match + num_if + if_let + num_while + num_loop
    match_ratio = num_match / max(cond_total, 1)

    return {
        "lines": num_l,
        "blanks": num_b,
        "comment ratio": comment_r,
        "line length": avg_l_len,
        "indent variations": indent_var,
        "functions": num_funcs,
        "structs": num_structs,
        "enums": num_enums,
        "traits": num_traits,
        "impls": num_impls,
        "modules": num_mods,
        "use statements": num_use,
        "pub items": num_pub,
        "consts": num_const,
        "macros": num_macro,
        "tests": num_tests,
        "type annotations": type_annotations,
        "generics": generics,
        "lifetimes": num_lifetimes,
        "unsafe": unsafe,
        "matches": num_match,
        "match ratio": match_ratio,
        "questions": num_questions,
        "if_let": if_let,
        "loops": num_loop,
        "avg ident len": avg_ind_len,
        "todo comments": num_todo,
        "doc comments": doc_comms,
        "code": code,
    }


file_path = sys.argv[1]
with open(file_path, encoding="utf-8") as f:
    code = f.read()

f = features(code)
renamed = {
    "num_l": f["lines"],
    "num_b": f["blanks"],
    "comment_r": f["comment ratio"],
    "avg_l_len": f["line length"],
    "indent_var": f["indent variations"],
    "num_funcs": f["functions"],
    "structs": f["structs"],
    "enums": f["enums"],
    "traits": f["traits"],
    "impls": f["impls"],
    "modules": f["modules"],
    "use statements": f["use statements"],
    "pub items": f["pub items"],
    "consts": f["consts"],
    "macros": f["macros"],
    "tests": f["tests"],
    "type annotations": f["type annotations"],
    "generics": f["generics"],
    "lifetimes": f["lifetimes"],
    "unsafe": f["unsafe"],
    "matches": f["matches"],
    "match ratio": f["match ratio"],
    "questions": f["questions"],
    "if_let": f["if_let"],
    "loops": f["loops"],
    "avg ident len": f["avg ident len"],
    "todo comments": f["todo comments"],
    "doc comments": f["doc comments"],
    "code": f["code"],
}
df = pd.DataFrame([renamed])

pipeline = joblib.load("models/rust.pkl")
prediction = pipeline.predict(df)[0]
prob = pipeline.predict_proba(df)[0]

if prediction == 1:
    label = "AI"
    confidence = prob[1] * 100
else:
    label = "human"
    confidence = prob[0] * 100

print(f"{file_path} is {confidence:.2f}% likely to be {label}")

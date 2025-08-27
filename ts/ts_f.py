# ts feature extraction

import os
import csv
import re

root = os.path.dirname(os.path.dirname(__file__))

ai_dataset = os.path.join(root, "dataset", "ts", "ai")
human_dataset = os.path.join(root, "dataset", "ts", "human")
csv_path = os.path.join(root, "dataset", "ts.csv")


def features(code):
    lines = code.splitlines()
    num_l = len(lines)
    num_b = sum(1 for l in lines if not l.strip())

    # no of lines that are comments
    comment_l = 0
    for i in lines:
        strip = i.strip()
        if strip.startswith("//"):
            comment_l += 1
        if strip.startswith("/*"):
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

    # functions
    func_pattern = (
        r"\bfunction\b|\basync\b\s*(function)?|\b\w+\s*\([^)]*\)\s*:\s*\w+\s*{|=>"
    )

    num_funcs = len(re.findall(func_pattern, code))
    num_arrows = len(re.findall(r"=>", code))
    arrow_r = num_arrows / max(num_funcs + num_arrows, 1)
    vars_funcs = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", code)
    avg_ind_len = sum(len(n) for n in vars_funcs) / max(len(vars_funcs), 1)

    num_interfaces = len(re.findall(r"\binterface\b", code))
    num_types = len(re.findall(r"\btype\b", code))
    num_enums = len(re.findall(r"\benum\b", code))
    num_classes = len(re.findall(r"\bclass\b", code))
    num_imports = len(re.findall(r"\bimport\b", code))
    num_exports = len(re.findall(r"\bexport\b", code))
    type_annotations = len(re.findall(r":\s*[A-Za-z_][A-Za-z0-9_<>,\[\]\s]*", code))
    generics = len(re.findall(r"<[A-Za-z_][A-Za-z0-9_,\s]*>", code))

    access_mods = len(re.findall(r"\b(public|private|protected|readonly)\b", code))

    vars_funcs = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", code)

    return {
        "lines": num_l,
        "blanks": num_b,
        "comment ratio": comment_r,
        "line length": avg_l_len,
        "indent variations": indent_var,
        "functions": num_funcs + num_arrows,
        "arrow ratio": arrow_r,
        "avg ind len": avg_ind_len,
        "code": code,
        "interfaces": num_interfaces,
        "types": num_types,
        "enums": num_enums,
        "classes": num_classes,
        "imports": num_imports,
        "exports": num_exports,
        "type annotations": type_annotations,
        "generics": generics,
        "access modifiers": access_mods,
    }


if not os.path.isdir(human_dataset):
    raise FileNotFoundError(human_dataset)

fieldnames = ["filename", "label"] + list(features("").keys())

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for label, folder in [("ai", ai_dataset), ("human", human_dataset)]:
        for file in sorted(os.listdir(folder)):
            if not file.endswith(".ts"):
                continue

            path = os.path.join(folder, file)
            with open(path, encoding="utf-8") as f:
                code = f.read()
            feats = features(code)
            row = {"filename": file, "label": label, **feats}
            writer.writerow(row)
            print(file)

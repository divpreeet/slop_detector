# html feature extraction
import os
import csv
import ast
import re

ai_dataset = 'dataset/html/ai'
human_dataset = 'dataset/html/human'
csv_path = 'dataset/html.csv'

import re


# used AI to get more features, the current params werent enough. 
def features(code):
    lines = code.splitlines()
    num_lines = len(lines)
    num_blanks = sum(1 for l in lines if not l.strip())
    num_html_comments = len(re.findall(r'<!--', code))
    avg_line_length = sum(len(l) for l in lines) / max(num_lines, 1)
    indent_var = len(set(re.match(r'^(\s+)', l).group(1) if re.match(r'^(\s+)', l) else '' for l in lines))
    num_tags = len(re.findall(r'<([a-zA-Z0-9]+)[\s>]', code))
    tag_types = set(re.findall(r'<([a-zA-Z0-9]+)[\s>]', code))
    num_img = len(re.findall(r'<img\b', code))
    num_links = len(re.findall(r'<a\b', code))
    num_forms = len(re.findall(r'<form\b', code))
    num_scripts = len(re.findall(r'<script\b', code))
    num_styles = len(re.findall(r'<style\b', code))
    num_css_rules = len(re.findall(r'\{[^}]*\}', code))
    num_classes = len(re.findall(r'class="([^"]+)"', code))
    unique_classes = set(re.findall(r'class="([^"]+)"', code))
    use_flexbox = 'flex' in code
    use_grid = 'grid' in code
    emoji_count = len(re.findall(r'[^\w\s,]', code))
    meta_tags = len(re.findall(r'<meta\b', code))
    external_links = len(re.findall(r'https?://', code))
    aria_count = len(re.findall(r'aria-', code))
    data_attr_count = len(re.findall(r'data-', code))
    button_count = len(re.findall(r'<button\b', code))
    favicon = bool(re.search(r'<link[^>]+rel="icon"', code))
    google_fonts = bool(re.search(r'fonts\.googleapis\.com', code))
    semantic_tags = len(set(tag_types) & set(['main', 'section', 'article', 'header', 'footer', 'nav', 'aside']))
    inline_events = len(re.findall(r'on\w+="', code))
    minified = avg_line_length > 120  #guess
    
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', code)
    heading_text = ' '.join(headings)
    button_texts = re.findall(r'<button[^>]*>(.*?)</button>', code)
    button_text = ' '.join(button_texts)
    all_text = heading_text + ' ' + button_text
    ai_keywords = sum(word in all_text.lower() for word in ['ai', 'smart', 'intelligent', 'powered', 'chatgpt'])

    return {
        'lines': num_lines,
        'blanks': num_blanks,
        'html_comments': num_html_comments,
        'avg_line_length': avg_line_length,
        'indent_variations': indent_var,
        'tags': num_tags,
        'unique_tags': len(tag_types),
        'semantic_tags': semantic_tags,
        'imgs': num_img,
        'links': num_links,
        'forms': num_forms,
        'scripts': num_scripts,
        'styles': num_styles,
        'css_rules': num_css_rules,
        'classes': num_classes,
        'unique_classes': len(unique_classes),
        'use_flexbox': use_flexbox,
        'use_grid': use_grid,
        'emoji_count': emoji_count,
        'meta_tags': meta_tags,
        'external_links': external_links,
        'aria_count': aria_count,
        'data_attr_count': data_attr_count,
        'button_count': button_count,
        'favicon': favicon,
        'google_fonts': google_fonts,
        'inline_events': inline_events,
        'minified': minified,
        'ai_keywords': ai_keywords,
        'code': code,
}

if not os.path.isdir(human_dataset):
    raise FileNotFoundError(human_dataset)

fieldnames = ['filename', 'label'] + list(features("").keys())

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for label, folder in [('ai', ai_dataset), ('human', human_dataset)]:
        for file in sorted(os.listdir(folder)):
            if not file.endswith(".html"):
                continue
            
            path = os.path.join(folder, file)
            with open(path, encoding='utf-8') as f:
                code = f.read()
            feats = features(code)
            row = {"filename": file, "label": label, ** feats}
            writer.writerow(row)
            print(file)
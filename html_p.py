# html prediction
import sys
import pandas as pd
import joblib
import ast
import re

# from html features
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
    use_flexbox = int('flex' in code)
    use_grid = int('grid' in code)
    emoji_count = len(re.findall(r'[^\w\s,]', code))
    meta_tags = len(re.findall(r'<meta\b', code))
    external_links = len(re.findall(r'https?://', code))
    aria_count = len(re.findall(r'aria-', code))
    data_attr_count = len(re.findall(r'data-', code))
    button_count = len(re.findall(r'<button\b', code))
    favicon = int(bool(re.search(r'<link[^>]+rel="icon"', code)))
    google_fonts = int(bool(re.search(r'fonts\.googleapis\.com', code)))
    semantic_tags = len(set(tag_types) & set(['main', 'section', 'article', 'header', 'footer', 'nav', 'aside']))
    inline_events = len(re.findall(r'on\w+="', code))
    minified = int(avg_line_length > 120)
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', code)
    heading_text = ' '.join(headings)
    button_texts = re.findall(r'<button[^>]*>(.*?)</button>', code)
    button_text = ' '.join(button_texts)
    all_text = heading_text + ' ' + button_text
    ai_keywords = sum(word in all_text.lower() for word in ['ai', 'smart', 'intelligent', 'powered', 'chatgpt'])

    return {
        'num_lines': num_lines,
        'num_blanks': num_blanks,
        'num_html_comments': num_html_comments,
        'avg_line_length': avg_line_length,
        'indent_var': indent_var,
        'num_tags': num_tags,
        'tag_types': len(tag_types),
        'semantic_tags': semantic_tags,
        'num_img': num_img,
        'num_links': num_links,
        'num_forms': num_forms,
        'num_scripts': num_scripts,
        'num_styles': num_styles,
        'num_css_rules': num_css_rules,
        'num_classes': num_classes,
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


file_path = sys.argv[1]
with open(file_path, encoding='utf-8') as f:
    code = f.read()

features = features(code)
# renamed = {
#         'lines': features['num_lines'],
#         'blanks': features['num_blanks'],
#         'html_comments': features['num_html_comments'],
#         'avg_line_length': features['avg_line_length'],
#         'indent_variations': features['indent_var'],
#         'tags': features['num_tags'],
#         'unique_tags': features['tag_types'],
#         'semantic_tags': features['semantic_tags'],
#         'imgs': features['num_img'],
#         'links': features['num_links'],
#         'forms': features['num_forms'],
#         'scripts': features['num_scripts'],
#         'styles': features['num_styles'],
#         'css_rules': features['num_css_rules'],
#         'classes': features['num_classes'],
#         'unique_classes': features['unique_classes'],
#         'use_flexbox': features['use_flexbox'],
#         'use_grid': features['use_grid'],
#         'emoji_count': features['emoji_count'],
#         'meta_tags': features['meta_tags'],
#         'external_links': features['external_links'],
#         'aria_count': features['aria_count'],
#         'data_attr_count': features['data_attr_count'],
#         'button_count': features['button_count'],
#         'favicon': features['favicon'],
#         'google_fonts': features['google_fonts'],
#         'inline_events': features['inline_events'],
#         'minified': features['minified'],
#         'ai_keywords': features["ai_keywords"],
#         'code': features['code'],
# }

df = pd.DataFrame([features])

pipeline = joblib.load('html.pkl')

prediction = pipeline.predict(df)[0]

if prediction == 1:
    label = "AI"
else: 
    label = "human"

print(f"{file_path} is written by a {label}")
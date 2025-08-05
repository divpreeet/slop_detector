# html model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# dataframe
df = pd.read_csv('dataset/html.csv')

df = df.rename(columns={
        'lines':'num_lines',
        'blanks': 'num_blanks',
        'html_comments': 'num_html_comments',
        'avg_line_length': 'avg_line_length',
        'indent_variations': 'indent_var',
        'tags': 'num_tags',
        'unique_tags': 'tag_types',
        'semantic_tags': 'semantic_tags',
        'imgs': 'num_img',
        'links': 'num_links',
        'forms': 'num_forms',
        'scripts': "num_scripts",
        'styles': "num_styles",
        'css_rules': 'num_css_rules',
        'classes': "num_classes",
        'unique_classes': 'unique_classes',
        'use_flexbox': 'use_flexbox',
        'use_grid': 'use_grid',
        'emoji_count': 'emoji_count',
        'meta_tags': "meta_tags",
        'external_links': "external_links",
        'aria_count': "aria_count",
        'data_attr_count': 'data_attr_count',
        'button_count': 'button_count',
        'favicon': 'favicon',
        'google_fonts': 'google_fonts',
        'inline_events': 'inline_events',
        'minified': 'minified',
        'ai_keywords': "ai_keywords",
        'code': "code",
})

df['label'] = df['label'].map({'human': 0, 'ai': 1})

numerics = [
    'num_lines', 'num_blanks', 'num_html_comments', 'avg_line_length', 'indent_var', 'num_tags', 'tag_types', 'semantic_tags',
    'num_img', 'num_links', 'num_forms', 'num_scripts', 'num_styles', 'num_css_rules', 'num_classes', 'unique_classes', 'use_flexbox',
    'use_grid', 'emoji_count', 'meta_tags', 'external_links', 'aria_count', 'data_attr_count', 'button_count',
    'favicon', 'google_fonts', 'inline_events', 'minified', 'ai_keywords'
]

text = 'code'

X = df[numerics + [text]]
Y = df['label']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=12)

preprocess = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerics),
        ('tfidf', TfidfVectorizer(max_features=100), text),
    ]
)

# preprocess + classifier
pipeline = Pipeline([
    ('pre', preprocess),
    ('cf', RandomForestClassifier(n_estimators=100, random_state=12))
])

pipeline.fit(X_train, Y_train)

y_pred = pipeline.predict(X_test)

print(classification_report(Y_test, y_pred))

joblib.dump(pipeline, 'html.pkl')
# ts model
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

root = os.path.dirname(os.path.dirname(__file__)) 

# dataframe
df_path = os.path.join(root, 'dataset', 'ts.csv')
df = pd.read_csv(df_path)

df = df.rename(columns={
    'lines': "num_l",
    'blanks': "num_b",
    'comment ratio': "comment_r",
    'line length': "avg_l_len",
    'indent variations': "indent_var",
    'functions': "num_funcs",
    'arrow ratio': "arrow_r",
    'avg ind len': "avg_ind_len",
    'interfaces': 'num_interfaces',
    'types': 'num_types',
    'enums': 'num_enums',
    'classes': 'num_classes',
    'imports': 'num_imports',
    'exports': 'num_exports',
    'type annotations': 'type_annotations',
    'generics': 'generics',
    'access modifiers': 'access_mods',
})

df['label'] = df['label'].map({'human': 0, 'ai': 1})


numerics = [
    "num_l", "num_b", "comment_r", "avg_l_len", "indent_var", "num_funcs", "arrow_r", "avg_ind_len",
    'num_interfaces', 'num_types', 'num_enums', 'num_classes', 'num_imports', 'num_exports',
    'type_annotations', 'generics', 'access_mods'
]

text = "code"

X = df[numerics + [text]]
Y = df['label']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=12)

preprocess = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerics),
        ('tfidf', TfidfVectorizer(max_features=2000), text),
    ]
)

# preprocess + classifier
pipeline = Pipeline([
    ('pre', preprocess),
    ('cf', RandomForestClassifier(n_estimators=200, random_state=12))
])

pipeline.fit(X_train, Y_train)

y_pred = pipeline.predict(X_test)

print(classification_report(Y_test, y_pred))

joblib.dump(pipeline, 'models/ts.pkl')
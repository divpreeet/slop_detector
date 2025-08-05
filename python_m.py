# python model

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
df = pd.read_csv('dataset/python.csv')

df = df.rename(columns={
    'lines': "num_l",
    'blanks': "num_b",
    'comment ratio': "comment_r",
    'line length': "avg_l_len",
    'indent variations': "indent_var",
    'functions': "num_funcs"
})

df['label'] = df['label'].map({'human': 0, 'ai': 1})

numerics= ['num_l', 'num_b', 'comment_r', 'avg_l_len', 'indent_var', 'num_funcs']
text= 'code'

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

joblib.dump(pipeline, 'python.pkl')
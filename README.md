# slop detector


> [!NOTE]
> slop_detector is a ai code detector purely made in python, from the model training to the UI! currently this project supports rust, ts, js, and python, i dont really plan to extend it anymore. 

# how it works 
it's actually pretty simple, at first i gathered datasets for ai code and human written code, from claude, gpt, gemini, hc api, and github respectively, then i extract specific numeric features like ind_len, comment ratio, etc, from the code, i tried my best to keep the features vast and specific to the language it self. after getting features, i export them to a csv, and then use ```scikit-learn``` to train that data and make a model, the model's use the ```RandomForest Classifier``` and a ```TFid Vectorizer```. after that, i made a simple prediction script, which is really just extracting features from the code provided, and then runs it to the model using ```joblib``` and then the model provides an output!

i decided to make a flask app, since it would be more accessible, for that, i just made a simple flask function, which is essentially the same as the prediction code, but it just returns the prediction as a string, which i access through the flask app.

if you're interested, you can also check out the notes.md!

# try it out
the flask app is hosted on [nest]("https://slop.divpr.hackclub.app")

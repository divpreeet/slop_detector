# self-notes

- 2 - Aug - 2025
got 20 samples each, ai samples using ai hackclub, and manually got human datasets, also built feature extraction and got it to ouput .csv! in the format - 

```filename, label, lines, blanks, comment ratio, line length, indent variations, functions```

# model training
used scikit learn and dataframes with pd, and got a 1.00 for human code and 0.75 for ai, essentially i splitted the dataset X and Y, x for features and y for wether human or ai using the random forest classifier

also i got 410 samples each, for AI and human, scraped github for human, and used gemini 1.5 flash, claude and ai.hackclub to generate ai code. used tfidf to get a better result, ended up geting 97% accuracy!

# prediction
its prety simple, it extracts the feature from the code, and then pipes the model and uses joblib to load it! and then gets the prediction!


# todo
add html, css, js.
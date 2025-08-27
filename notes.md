# self-notes

- 2 - Aug - 2025
got 20 samples each, ai samples using ai hackclub, and manually got human datasets, also built feature extraction and got it to ouput .csv! in the format - 

```filename, label, lines, blanks, comment ratio, line length, indent variations, functions```

## model training
used scikit learn and dataframes with pd, and got a 1.00 for human code and 0.75 for ai, essentially i splitted the dataset X and Y, x for features and y for wether human or ai using the random forest classifier

also i got 410 samples each, for AI and human, scraped github for human, and used gemini 1.5 flash, claude and ai.hackclub to generate ai code. used tfidf to get a better result, ended up geting 97% accuracy!

## prediction
its prety simple, it extracts the feature from the code, and then pipes the model and uses joblib to load it! and then gets the prediction!

## scraper - updated
made it so we dont get 404 errors, list time i was construction a raw file url and then returning the code from there, turns out github has a search api which returns the base64 code, which you need to decode and then download!


## adding multiple language support
adding html support next, needed to change filenmames to stuff like ```python_f.py``` for feature extraction for python, need to really clean up the folder struct, really just reusing code at this point.

## html support
scraped 400 human samples from github, getting human samples isnt a problem, its seamless, ai smaples are a problem, got 200 from gemini, and the rest were from chatgpt 4.1, turns out if you have github edu, gpt 4.1 is free on gh copliot! trained the model, and it gets 97% accuracy!

needed to use AI to get a better result, since if prompted, you can easily pass the detector, even after using AI (and tons of fixing ai code), its still pretty dodgy and isnt that reliable, ig its because of the lack of proper data, and i currently wont be able to solve that without paying for an AI service, so ig, HTML detection would be marked as a rough estimate, and it can be pretty dodgy.

ended up removing html support, since its really finnicky, and unreliable, instead i am adding js support


## adding js support
got 408 files each of human (from gh) and ai (gemini, gpt 4.1, claude), then i just copy pasted the feature extraction and model training, getting a 96% accuracy! modified the feature extraction a bit to get the count of comment lines.

## adding ts support
getting human code and ai code.. seems like this is going to be pretty similar to the js detection, hope it doesnt take up my week lol


## adding rust support
this was by far the hardest thing to add, since i've never really programmed in rust, and dk the syntax that well, so had to skim through tons of ai rust code, github samples of rust code, and the rust book, i havent read the whole thing, but have a basic idea of how it now works, also asked the hc slack and got some tips there too!

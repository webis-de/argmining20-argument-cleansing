# Semi-Supervised cleansing of argument corpora

# Executing the code
In order to run the application, you can simply call the "main.py" from the
terminal. The current implementation is highly focussed on the args.me corpus
and therefore the implementation is matching the corpus structure.

In order for the code to run, the args.me corpus has to be added to
"/data/argsme". Otherwise paths in the main have to be adjusted.

Additionally, one might have to install some specific dependencies.
Besides the usual python modules (os, time, csv, json, etc.), especially 
"multiprocessing" (https://docs.python.org/2/library/multiprocessing.html), 
nltk (https://www.nltk.org/), spacy (https://spacy.io/) and 
Krippendorf (https://pypi.org/project/krippendorff/) are required.
For a full list of all dependencies please inspect the code directly.

All important steps are handled in the "main.py" and can be seperated as follows:
(Inspect main for further details)

1. corpus_processor:
    In this fnc the args.me corpus is read. Additionally, you have to comment in
    the "creator.initial_pattern_creator(corpus)" line to generate the
    lists which we used for manual pattern selection.
    In order to modify the creation parameters, please inspect "patterncreator.py".

2. main_processor:
    Specific parameters such as minimum pattern frequency and minimum precision
    can be specified for both positive and negative patterns individually at
    fnc call.
    Reads in the hand selected patterns from specified location.
    (Predefined as in our approach used. Change if wished)
    Automatically processes the corpus and extracts new sentences and patterns
    based on the hand selected list mentioned above.
    The main_processor will generate a multitude of files printed to a
    predefined location for the initial step, each iteration step and the
    final results of the approach. Inspect the specified path for results
    (default = /data/test_0.95-0.95-200-2000/)

3. post_processor:
    Removes all irrelevant sentences from the corpus.
    Last rounds results have to be specified here manually currently.
    Writes a clean version of the corpus to "/data/reworked_corpus.csv"
    In the current version additionally generated data in the JSON is not
    removed. Therefore corpus size increases significantly.


Since the prototype is designed to evaluate our approaches concept, it currently
does not support a full pipeline for the different pattern extraction approaches
besides "n-gram no stopwords". However, the initial pattern lists can be
generated for all different approaches.

In case one wants to modify the range in which n_grams are generated, the
"n_gram_range" in "pattern_creator.py/create_new_pattern" or respectively the
loop in "pattern_creator.py/initial_pattern_creator" has to be adjusted.

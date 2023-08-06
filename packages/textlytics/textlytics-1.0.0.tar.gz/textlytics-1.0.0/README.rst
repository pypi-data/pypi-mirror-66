Text Analytics Toolkit (textlytics)
====================================

TEXTLYTICS -- the Text Analytics Toolkit -- is a suite of open source Python modules
supporting research and development in Text Analytics, more specifically,
how to measure textual complexity for english and portuguese documents.

https://gitlab.com/jorgeluizfigueira/python-textlytics/

This toolkit is a project under development, the result of studies in textual complexity 
analysis research. The library provides several methods for extracting characteristics 
based on word occurrence metrics. Additionally, the counting of popular part of speech 
tagging, such as verbs, adjectives, nouns, were added. Studies carried out with such 
characteristics indicate that they can be used as a structured representation capable 
of increasing the accuracy of text document classification systems.

Dependencies:

This Toolkit requires the following dependencies:

* requests
* json
* tqdm
* pandas
* regex
* nltk
* nlpnet
* pyphen
* syllabes

The nlpnet library requires additional files to do parts of speech tagging for documents in Portuguese.
Use the download ('pos-pt') method to get them and config.setPosPtDir () to set the file path

Features:

* Statistical features:
* Number of characters
* Number of words
* Average word size
* Number of unique words (vocabulary)
* Number of sentences
* Average words per sentence
* Number of syllables
* Average syllables per word
* Rate of rare words (words that occur only once)
* Lexical Diversity
* Readability
* Schooling according to Readability
* Part of Speech Tagging Counter:
* Incidence of Verbs, Adjectives, Nouns, Pronouns and Connectives
* Content Incidence
* Content Diversity

Usage:

>>> import textlytics
>>> textlytics.config.setLanguage('english')
>>> textlytics.config.setIncidence(1)
>>> textlytics.download('pos-pt')
'Downloading from https://textlytics.webs.com/metadata-pos.pickle: 1KB [00:00, 433.30KB/s]  '                       
'Download complete!'
'Downloading from https://textlytics.webs.com/pos-network.npz: 63075KB [03:03, 343.38KB/s]   '                                   
'Download complete!'
'Downloading from https://textlytics.webs.com/pos-tags.txt: 1KB [00:00, 384.48KB/s]'
'Download complete!'
'Downloading from https://textlytics.webs.com/prefixes.txt: 13KB [00:00, 3653.57KB/s]'
'Download complete!'
'Downloading from https://textlytics.webs.com/suffixes.txt: 10KB [00:00, 3305.99KB/s]'
'Download complete!'
'Downloading from https://textlytics.webs.com/vocabulary.txt: 697KB [00:02, 319.21KB/s]'
'Download complete!'
>>> textlytics.config.setPosPtDir()
>>> text = "Computational techniques can be used to identify musical trends and patterns,
    helping people filtering and selecting music according to their preferences. In this scenario,
    researches claim that the future of music permeates artificial intelligence, which will play 
    the role of composing music that best fits the tastes of consumers. So, extracting patterns 
    from this data is critical and can contribute to the music industry ecosystem. These techniques
    are well known in the field of Musical Information Retrieval. They consist of the audio
    characteristics extraction  (content) or lyrics (context), being the latter preferable because 
    it demands lower computational cost and presenting better results. However, when observing state 
    of the art, it was found that there is a lack of antecedents that investigate the extraction of Brazilian 
    music patterns through lyrics. In this sense, the main goal of this work is to fill this gap through text
    mining techniques, analyzing the songs classification in the subgenres of Brazilian country music.
    This analysis is based on lyrics and knowledge extraction to explain how subgenres differ."
>>> textlytics.charCounter(text)
1118
>>> textlytics.avgWordLen(text)
5.476744186046512
>>> textlytics.wordCounter(text)
172
>>> textlytics.uniqueWordsCounter(text)
114
>>> textlytics.sentencesCounter(text)
8
>>> textlytics.avgWordsSentence(text)
21.5
>>> textlytics.syllableCounter(text)
290
>>> textlytics.avgSyllableWords(text)
1.686046511627907
>>> textlytics.rareWordsRatio(text)
0.5232558139534884
>>> textlytics.lexical_diversity(text)
0.6627906976744186
>>> textlytics.readability(text)
42.37296511627909
>>> textlytics.readability_schoolarity(text)
'College'
>>> textlytics.posTaggerCounter(text,'VERB')
34.0
>>> textlytics.posTaggerCounter(text,'ADJ')
12.0
>>> textlytics.posTaggerCounter(text,'N')
57.0
>>> textlytics.posTaggerCounter(text,'PRON')
4.0
>>> textlytics.posTaggerCounter(text,'CONTENT')
103.0
>>> textlytics.posTaggerCounter(text,'CONTENT-D')
0.5988372093023255
>>> # There is a special method that takes a  
>>> # dataframe and extracts all textual features,
>>> # according a name field (dataframe column).
>>> # features2Dataframe(dataframe,fieldName)
>>>
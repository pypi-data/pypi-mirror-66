This package allows you to automatically collect POS tagging results from http://ucrel-api.lancaster.ac.uk/claws/free.html and save them as txt files in your local folder.

Make sure to place your python file in a folder that contains (only) the txt files you wanna tag.

># example.py
># example.txt

>from CLAWSTag import Tagger

># There're 5 possible combos for tagsets ('c5' or 'c7') and output styles ('horiz(ontal)' or 'vert(ical)' or '(pseudo)xml'):
>Tagger.Postag('c5', 'horiz').start()
># Tagger.Postag('c5', 'xml').start()
># Tagger.Postag('c7', 'horiz').start()
># Tagger.Postag('c7', 'vert').start()
># Tagger.Postag('c7', 'xml').start()


>## OUTPUT: Tagged_example.txt
import setuptools

long_description = '''This package allows you to automatically collect POS tagging results from http://ucrel-api.lancaster.ac.uk/claws/free.html and save them as txt files in your local folder.

Make sure to place your python file in a folder that contains (only) the txt files you wanna tag.

Example:
>from CLAWSTag import Tagger

>Tagger.Postag('c5', 'horiz').start()

There're 5 possible combos for Postag() to receive settings of tagsets ('c5' or 'c7') and output styles ('horiz(ontal)' or 'vert(ical)' or '(pseudo)xml'). The others are:

Tagger.Postag('c5', 'xml').start()

Tagger.Postag('c7', 'horiz').start()

Tagger.Postag('c7', 'vert').start()

Tagger.Postag('c7', 'xml').start()
'''

setuptools.setup(
    name="CLAWSTag",
    version="0.0.2.1",
    author="VictorWWQ",
    author_email="VictorWWQ@163.com",
    description="an English POS tagging tool based on the free CLAWS web tagger API by Lancaster University",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'beautifulsoup4', 'Faker'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

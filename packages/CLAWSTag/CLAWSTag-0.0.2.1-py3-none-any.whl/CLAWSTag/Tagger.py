import requests, os, time, re
from bs4 import BeautifulSoup
from faker import Faker

class Postag:
    def __init__(self, tagset, style):
        if tagset not in ['c5', 'c7']:
            print('ERROR: The first parameter for postag() is expected to be "c5" or "c7" as a string.')
        elif tagset == 'c5' and style == 'vert':
            print('ERROR: Tagset "c5" does not support vertical output. Please try "c7" instead.')
        else:
            if style not in ['horiz', 'vert', 'xml']:
                print('ERROR: The second parameter for postag() is expected to be "horiz" or "vert" or "xml" as a string.')
            else:
                self.txt_files = [i for i in os.listdir(os.getcwd()) if i.endswith('.txt')]
                self.url = 'http://ucrel-api.lancaster.ac.uk/cgi-bin/claws74.pl'
                self.tagset = tagset
                self.style = style
    def start(self):
        for txt_file in self.txt_files:
            text = open(txt_file, 'r', encoding='utf-8').read()
            text_list = []
            if len(text) > 100000:
                if len(text) % 100000 != 0:
                    start = 0
                    end = 100000
                    for i in range((len(text)//100000)):
                        text_list += [text[start:end]]
                        start += 100000
                        end += 100000
                    text_list += [text[start:]]
                else:
                    start = 0
                    end = 100000
                    for i in range((len(text)//100000)):
                        text_list += [text[start:end]]
                        start += 100000
                        end += 100000
            else:
                text_list += [text]
                
            tagged_text_list = []
            for text in text_list:
                files = {
                    'email': (None, 'a.nobody@here.ac.uk'),
                    'tagset': (None, self.tagset),
                    'style': (None, self.style),
                    'text': (None, text)
                         }
                headers = {'User-Agent': Faker().chrome()}
                res = requests.post(self.url, headers=headers, files=files)
                soup = BeautifulSoup(res.text, 'html.parser')
                tagged_text = soup.find('pre').text
                tagged_text = re.sub(r'\**.*?TOOLONG_UNC', '', tagged_text)
                tagged_text_list += [tagged_text]

            Tagged_Text = ' '.join(tagged_text_list)
            with open('Tagged_' + txt_file, 'w', encoding='utf-8') as f:
                f.write(Tagged_Text)
            print(txt_file + ' tagged')

            time.sleep(1)

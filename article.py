import re

class Article:
    def __init__(self, record, nlp):
        self.title = record.find('./titles/title').text
        self.authors = [author.text for author in record.findall('./contributors/authors/author')]
        self.keywords = [keyword.text for keyword in record.findall('./keywords/keyword')]
        self.abstract = re.sub(r'<.*?>', '', record.find('./abstract').text)
        self.parse = nlp(self.abstract)
        doi = record.find('./electronic-resource-num')
        self.doi = doi.text if doi != None else ''

    def tokens(self, lower=False, no_punct=True, no_stop=True):
        ''' return abstract as tokens '''
        token_list = []
        for token in self.parse:
            if token.is_punct and no_punct:  # skip punctuation when needed
                continue
            if token.is_stop and no_stop:  # skip stop words when needed
                continue
            if token.is_space:  # always skip white space
                continue
            if lower:
                token_list.append(token.text.lower())
            else:
                token_list.append(token.text)
        return token_list

    def __str__(self):
        s = 'Title: {}\nAuthors: {}\nAbstract: {}\nDOI: {}'.format(self.title, \
            ', '.join(self.authors), self.abstract, self.doi)
        return s

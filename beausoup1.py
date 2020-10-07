from bs4 import BeautifulSoup
import unittest
import re

def recurse_headers(parent):
    try:
        list = parent.contents
    except AttributeError:
        return False
    for child in list:
        try:
            if child.string[0] == 'E' or child.string[0] == 'T' or child.string[0] == 'C':
                return True
            else:
                f = recurse_headers(child)
                if f:
                    return True
        except (AttributeError, TypeError):
            f = recurse_headers(child)
            if f:
                return True
    return False


def parse(path_to_file):
    imgs = 0
    headers = 0
    with open(path_to_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    body = soup.find('div', id='bodyContent')
    for tag in body.find_all('img'):
        try:
            if tag['width'] and int(tag['width'])>=200:
                imgs += 1
        except KeyError:
            pass
    for parent in body.find_all(name=re.compile(r'^h\d')):
        acc = recurse_headers(parent)
        if acc:
            headers += 1
    list_a = []
    for tag_a in body.find_all('a'):
        count_a = 1
        for sibling in tag_a.next_siblings:
            if sibling.name == None:
                pass
            elif sibling.name == 'a':
                count_a += 1
            else:
                break
        list_a.append(count_a)
    linkslen = max(list_a)
    lists = 0
    for tag_list in body.find_all(re.compile(r'[uo]l')):
        parents = [i.name for i in tag_list.parents]
        if parents.count('ul') == 0 and parents.count('ol') == 0:
            lists += 1
    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
         test_cases = (
             ('wiki/Stone_Age', [13, 10, 12, 40]),
             ('wiki/Brain', [19, 5, 25, 11]),
             ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
             ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
             ('wiki/Spectrogram', [1, 2, 4, 7]),
             ('wiki/Joseph_Stiglitz', [4, 16, 9, 87]),)

         for path, expected in test_cases:
             with self.subTest(path=path, expected=expected):
                 self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()

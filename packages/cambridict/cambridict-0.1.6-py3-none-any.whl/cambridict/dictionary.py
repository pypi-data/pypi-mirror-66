import lxml.html
import requests
import yaml

from . import const as CONST


class Dictionary(object):

    def __init__(self, **kw):
        self.link, self.structure = '', {}
        for name, value in kw.items():
            setattr(self, name, value)

    def search(self, word):
        url = self.link.format(word=word)
        r = requests.get(url)
        return self.parse(r.content)

    def parse(self, text):
        tree = lxml.html.fromstring(text)
        return self.__parse(tree, self.structure)

    def __parse(self, tree, kw):

        if CONST.CSS in kw:
            kw = kw.copy()
            sel = kw.pop(CONST.CSS, None)
            rst = self.__find(tree, sel)
            data = [self.__parse(child, kw) for child in rst]
            data = [el for el in data if len(el) > 0]

            if CONST.CLIST not in sel:
                data.append({})
                data = data[0]

        else:
            data = {}
            for key, value in kw.items():
                if isinstance(value, dict):
                    rst = self.__parse(tree, value)
                else:
                    rst = self.__find(tree, value)
                    rst = [self.__get_text(child) for child in rst]

                    if CONST.CLIST not in value:
                        rst = ' '.join(rst[:1])

                if len(rst) > 0 or CONST.CBLANK in value:
                    data[key] = rst

        return data

    def __find(self, tree, sel):
        selector = sel.split('@')[0]
        rst = tree.cssselect(selector)
        if CONST.CLIST not in sel:
            rst = rst[:1]
        return rst

    def __get_text(self, node):
        text = node.text_content()
        text = text.replace('\n', ' ')
        while ' '*2 in text:
            text = text.replace(' '*2, ' ')
        return text.strip()


class Cambridge(Dictionary):

    cambridge_yaml = CONST.CAMBRIDGE_YAML

    def __init__(self, dictname='EE'):
        with open(self.cambridge_yaml) as stream:
            config = yaml.safe_load(stream)
        dictname = config.get('dictionary', {}).get(dictname, dictname)
        kw = config.get(dictname)
        super().__init__(**kw)

# Python
#
# This module implements a text class that allows to modify and create text on Markdown files.
#
# This file is part of mdutils. https://github.com/didix21/mdutils
#
# MIT License: (C) 2020 Dídac Coll
from mdutils.tools.tools import TextUtils

class Reference(object):

    def __init__(self):
        self.references = {}

    def get_references(self):
        return self.references

    def get_references_as_markdown(self):
        if not bool(self.references):
            return ""

        references_as_markdown = ""
        for key in sorted(self.references.keys()):
            references_as_markdown += '[' + key + ']: ' + self.references[key] + '\n'
        return '\n\n\n' + references_as_markdown

    def new_link(self, link, text, reference_tag=None):

        if reference_tag is None:
            self.__update_ref(link, text)
            return '[' + text + ']'

        self.__update_ref(link, reference_tag)
        return '[' + text + '][' + reference_tag + ']'

    def __update_ref(self, link, reference_tag):
        if not (reference_tag in self.references.keys()):
            self.references.update({reference_tag: link})


class Inline:

    @staticmethod
    def new_link(link, text=None):
        if text is None:
            text = link
        return '[' + text + '](' + link + ')'

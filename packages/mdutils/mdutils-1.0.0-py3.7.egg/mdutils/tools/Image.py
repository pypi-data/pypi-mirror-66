# Python
#
# This module implements a text class that allows to modify and create text on Markdown files.
#
# This file is part of mdutils. https://github.com/didix21/mdutils
#
# MIT License: (C) 2020 Dídac Coll

from mdutils.tools.Link import Inline


class Image:

    @staticmethod
    def new_image(text, path):
        return "!" + Inline.new_link(link=path, text=text)



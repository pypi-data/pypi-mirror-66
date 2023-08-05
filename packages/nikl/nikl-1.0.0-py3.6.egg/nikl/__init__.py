# !/usr/bin/env python
# -*- coding: utf-8 -*-


__name__ = 'nikl'
__description__ = 'Preprocess NIKL(National Institute of Korean Language) Corpus files'
__version__ = '1.0.0'
__url__ = 'https://github.com/study-artificial-intelligence/nikl'
__download_url__ = 'https://github.com/study-artificial-intelligence/nikl'
__install_requires__ = [
    "beautifulsoup4",

]
__license__ = 'MIT'


from nikl.loader.load_file import *
from nikl.preprocessor import *
from nikl.target.infos import *
from nikl.target.contents import *
from nikl.option import *

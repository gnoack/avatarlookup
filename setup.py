#!/usr/bin/python2
# -*- encoding:utf-8 -*-
from setuptools import setup, find_packages
setup(
    name = "avatar_lookup",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["vobject >= 0.9.1"],
    entry_points = {
        "console_scripts": [
            "avatar-lookup = avatars.lookup:main",
            "avatar-index = avatars.index:main",
        ]
    },

    author = "Günther Noack",
    author_email = "guenther@unix-ag.uni-kl.de",
    description = "A cache of user Avatars integrated with VCard and mutt.",
    # long_description = "TODO",
    license = "Apache",
    keywords = "xface mutt vcard",
    # url = "TODO",
)

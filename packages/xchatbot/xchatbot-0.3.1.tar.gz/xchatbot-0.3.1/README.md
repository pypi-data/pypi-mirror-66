# The Xtensible XMPP Chat Bot

`XChatBot` is a xmpp bot library written in python using the 
[nbxmpp library from Gajim](https://dev.gajim.org/gajim/python-nbxmpp/)

![](https://readthedocs.org/projects/xchatbot/badge/?version=latest)  
[https://xchatbot.readthedocs.io/](https://xchatbot.readthedocs.io/)

## requirements

- python 3
- pygobject
- nbxmpp

optionally

- pipenv

## install

    pip install xchatbot

## git

    git clone https://git.sr.ht/~fabrixxm/xchatbot

install required packages:

**with pipenv**

    $ pipenv --site-packages --python 3
    $ pipenv install
    $ pipenv run ./xchatbot.py

**on osx** you need first to install python3 with brew:

    $ brew install python3 pipenv pygobject3

**on Arch**

    # pacman -S python-gobject python-nbxmpp

**on Debian**

    # apt install python3-gi python3-nbxmpp



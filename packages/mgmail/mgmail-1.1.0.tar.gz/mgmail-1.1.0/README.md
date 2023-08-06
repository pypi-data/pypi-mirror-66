MgMail
============

Simple command line utility which will import document attachments from SMTP account into a [Papermerge Project instance](https://github.com/ciur/papermerge) via REST API

It connects to IMAP account (your email account) via provided username/password/imap_server and iterates through all *unread* email messages.

For every unread message, if it finds a file attachment - it (mg-mail) uploads it via REST API to the papermerge service.

## Installation

    pip install mgmail


## Usage

Create a configuration file e.g. mgmail.config.py
Run::
    
        mgmail_imp --config /path/to/config.py

## Configuration file


Configuration file must have .py extention and be a valid python file, example::

    imap_server = "mail.paper.net"
    username = "<username>"
    password = "<pass>"
    api_key = "<API KEY>"
    papermerge_url = "<URL>"  # e.g. http://localhost:8000

## Configuration Settings
    
* ``imap_server`` is, well, your imap server.
* ``username`` and ``password`` - your imap user account
* ``api_key`` is papermerge's API key. Get your api_key as explained [here](https://papermerge.readthedocs.io/en/latest/rest_api.html#get-a-token)
* ``papermerge_url`` - paparmerge server instance url (with scheme i.e with http:// or https:// prefix). E.g. http://localhost:8000


## Configuration Logging

Logging configuration are read from mgmail.logging.yml file. Example of mgmail.logging.yml file::

    version: 1
    handlers:
      xyzconsole:
        class : logging.StreamHandler
    root:
      level: DEBUG
      handlers: [xyzconsole]

Example above configures root log to DEBUG level. All log messages will be displayed in console.
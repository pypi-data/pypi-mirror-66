==============
ConsoleDialogs
==============

A pure console replacement for the Robot Framework Dialogs library that uses
curses when installed, and otherwise falls back to ``raw_input(...)`` based
dialogs.

ConsoleDialogs has exactly the same API as the builtin `Dialogs library
<http://robotframework.org/robotframework/latest/libraries/Dialogs.html>`_.

Installation
============

.. code:: console

   git clone <git-url> # Get the git URL at Github page of this project
   cd robotframework-consoledialogs
   python setup.py install

Usage
=====

.. code:: robotframework

   *** Settings ***
   Library  ConsoleDialogs

   *** Test Cases ***
   Test Manual Step
       Execute Manual Step

   Test Selection From User
       ${username}=     Get Selection From User     Select user name    user1   user2   admin

   Test Value From User
       ${value}=        Get Value From User     Provide a name      default value
       ${secret}=       Get Value From User     Provide a password  hidden=yes

   Test pause Execution
       Pause Execution
       Pause Execution  message=Execution stopped. Hit [Return] to continue.

Links
=====

PyPI

  https://pypi.python.org/pypi/robotframework-consoledialogs

Source code

  https://github.com/tw39124-1/robotframework-consoledialogs

Issues tracker

  https://github.com/tw39124-1/robotframework-consoledialogs/issues

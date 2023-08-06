# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_gui']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.3.15,<3.0.0']

setup_kwargs = {
    'name': 'arcade-gui',
    'version': '0.1.0a4',
    'description': 'GUI extension for the Python game library Arcade  https://arcade.academy/',
    'long_description': "[![Build Status](https://travis-ci.org/eruvanos/arcade_gui.svg?branch=master)](https://travis-ci.org/eruvanos/arcade_gui)\n\n# GUI Library for Python Arcade\n\nThis project targets to offer simple to complex ui elements\nto use in games and software written with the Python Arcade library.\n\nSome UI components were copied over to adjust and fix them.\n\nThis project could also end up in a PR to integrate within Arcade.\n\n## Basic Components\n\n#### UIView\nCentral class to manager the ui components.\nConverts `on_` callback functions into events, so that UIElements\njust have to contain one method to interact with user input.\n\n#### UIElement\nA general interface of an UI element.\n\n## Examples\n\nExamples providing an overview of features, there will be dedicated documentation soon.\n\n* [UILabel](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uilabel.py)\n* [UIButton](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uibutton.py)\n* [UIInputBox](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uiinputbox.py)\n* [Example with ID](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_id_example.py)\n\n### Screenshots\n\n![Example with ID Screenshot](https://github.com/eruvanos/arcade_gui/blob/master/docs/assets/ProGramer.png)\n\n\n## Features for first release\n\n* [x] UILabel\n    * [x] Align with UITextInput\n* [x] UIButton\n* [x] Focused element tracked\n* [x] ID reference system for UIElements\n* [x] CI/CD\n* [x] UITextInput\n    * [x] Basic setup\n    * [ ] Scroll text with cursor\n    * [ ] Set max length\n    * [ ] Emit event on ENTER\n* [ ] UIElements emit own UIEvents\n    * [x] UIButton\n    * [ ] UITextInput\n* [ ] UIImageButton\n* [ ] UITexturedInputBox\n* [ ] FlatButtons (https://codepen.io/maziarzamani/full/YXgvjv)\n* [ ] UITextArea\n* [ ] Theme support\n    * [ ] Provide different standard themes for flat buttons\n* [ ] Add documentation and doc strings (sphinx)\n    * [ ] release notes\n    * [ ] setup readthedocs\n* [ ] track new features and issues in Github\n\n### Chores\n\n* [ ] harmonize constructors `x, y` vs `center_x, center_y`\n* [ ] figure out, how `UIView.find_by_id` does not produce typing warnings\n* [ ] improve docs\n    * [x] fix reference to examples\n    * [x] include screenshots (at least one)\n* [ ] make 3D Button more realistic, or change to flat buttons\n* [ ] support Python 3.7\n* [x] test examples render the expected screen\n\n## Background information and other frameworks\n\n### Reference Pygame GUI projects\n\n[Overview](https://www.pygame.org/wiki/gui)\n\n* ThorPy\n    * http://www.thorpy.org/index.html\n* Phil's pyGame Utilities\n    * https://www.pygame.org/project/108\n* OcempGUI\n    * https://www.pygame.org/project/125\n* PyGVisuals\n    * https://github.com/Impelon/PyGVisuals\n* Pygame GUI\n    * [Homepage](https://github.com/MyreMylar/pygame_gui)\n    * [Examples](https://github.com/MyreMylar/pygame_gui_examples)\n    * [QuickStart Example](https://github.com/MyreMylar/pygame_gui_examples/blob/master/quick_start.py)\n    * Concept\n        * UIManager manages every interaction, new elements get the UIManager on creation\n        * Elements create events and hook into pygames event system\n        * Themes can be read from JSON files\n\n\n### Ideas\n* Create own implementation\n* Build adapter for PyGame GUI",
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/arcade_gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

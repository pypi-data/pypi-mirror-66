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
    'version': '0.1.0a1',
    'description': 'GUI extension for the Python game library Arcade  https://arcade.academy/',
    'long_description': "# GUI Library for Python Arcade\n\nThis project targets to offer simple to complex ui elements\nto use in games and software written with the Python Arcade library.\n\nSome UI components were copied over to adjust and fix them.\n\nThis project could also end up in a PR to integrate within Arcade.\n\n## Basic Components\n\n#### UIView\nCentral class to manager the ui components.\nConverts `on_` callback functions into events, so that UIElements\njust have to contain one method to interact with user input.\n\n#### UIElement\nA general interface of an UI element.\n\n## Examples\n\n* [UILabel](./examples/show_uilabel.py)\n* [UIButton](./examples/show_uibutton.py)\n\n\n## Features for first release\n\n* [x] UILabel\n    * [ ] Align with UITextInput\n* [x] UIButton\n* [x] Focused element tracked\n* [x] UITextInput\n    * [x] Basic setup\n    * [ ] Textured frame\n    * [ ] Scroll text with cursor\n    * [ ] Set max length\n    * [ ] Emit event on ENTER\n* [ ] UIImageButton\n* [ ] UITextArea\n* [ ] UIElements emit own UIEvents\n* [ ] Theme support\n\n### Chores\n\n* [ ] harmonize constructors `x, y` vs `center_x, center_y`\n* [ ] improve docs\n    * [ ] setup readthedocs\n    * [ ] fix reference to examples\n\n## Background information and other frameworks\n\n### Reference Pygame GUI projects\n\n[Overview](https://www.pygame.org/wiki/gui)\n\n* ThorPy\n    * http://www.thorpy.org/index.html\n* Phil's pyGame Utilities\n    * https://www.pygame.org/project/108\n* OcempGUI\n    * https://www.pygame.org/project/125\n* PyGVisuals\n    * https://github.com/Impelon/PyGVisuals\n* Pygame GUI\n    * [Homepage](https://github.com/MyreMylar/pygame_gui)\n    * [Examples](https://github.com/MyreMylar/pygame_gui_examples)\n    * [QuickStart Example](https://github.com/MyreMylar/pygame_gui_examples/blob/master/quick_start.py)\n    * Concept\n        * UIManager manages every interaction, new elements get the UIManager on creation\n        * Elements create events and hook into pygames event system\n        * Themes can be read from JSON files\n\n\n### Ideas\n* Create own implementation\n* Build adapter for PyGame GUI",
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/arcade_gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

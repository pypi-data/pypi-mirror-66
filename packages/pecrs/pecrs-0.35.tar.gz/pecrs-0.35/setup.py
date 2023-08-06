# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pecrs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pecrs',
    'version': '0.35',
    'description': 'Pythonic Entity Collision Resolution System',
    'long_description': '![logo](https://raw.githubusercontent.com/solidsmokesoftware/pecrs-py/master/logo.png)\n\n# Pythonic Entity Collision Resolution System\n\npecrs is a pure Python 2D physics system with a focus on top-down games and simple platformers. \n\nPure Python makes pecrs portable and easy to modify to suit your own needs.\n\nFocused use-case makes pecrs simple to learn and use.\n\n[Seamless integration](https://solidsmokesoftware.github.io/pecrs-py/pyglet.html) with [Pyglet](http://pyglet.org/)\n\n# Installation\n\nVia pip\n\n`python3 -m pip install pecrs`\n\n# Quickstart\n```python\n\nfrom pecrs import *\n\nspace = Space()\nrectA = Rect(0, 0, 32, 32)\nrectB = Rect(10, 0, 32, 32)\n\nspace.add(rectA)\nspace.add(rectB)\n\ncollision = space.check(rectA)\nprint(f"Is something colliding with rectA? {collision}")\n\ncollisions = space.collisions_with(rectB)\nprint(f"Who is colliding with rectB? {collisions}")\n\nspace.place(rectB, 100, 0)\n\ncollision = space.check_two(rectA, rectB)\nprint(f"Are rectA and rectB still colliding? {collision}")\n```\n\n# Structual Overview\n\nBase types of the system are Shapes and Bodies. \nShapes have a position and dimensions which describe its physical properties.\nBodies are Shapes with an id, direction, speed, and movement state.\n\nCore functionality is providied by the Collider, which detects collisions between Shapes or Shape-like Objects.\n\nThe Space handles positioning of Shapes and optimizes collision handling.\n\nThe Controller provides high-level object oriented control over Bodies in a Space.\n\n# Real-world Usage\n\n![demo](https://raw.githubusercontent.com/solidsmokesoftware/pecrs-py/master/pyglet_demo.gif)\n\n```python\n\nfrom pecrs import *\nimport pyglet\n\n\nclass World(Space):\n   def __init__(self):\n      super().__init__()\n      self.window = pyglet.window.Window(400, 300)\n      self.batch = pyglet.graphics.Batch()\n      \n      self.red_image = pyglet.resource.image("red_rect.png")\n      self.blue_image = pyglet.resource.image("blue_rect.png")\n\n      spriteA = pyglet.sprite.Sprite(self.blue_image, x=0, y=150, batch=self.batch)\n      spriteB = pyglet.sprite.Sprite(self.blue_image, x=300, y=150, batch=self.batch)\n\n      self.add(spriteA, moving=True)\n      self.turn(spriteA, (150, 0))\n\n      self.add(spriteB)\n      \n      pyglet.clock.schedule_interval(self.run, 1.0/60)\n      pyglet.app.run()\n\n   def on_collision(self, shape, collisions):\n      shape.image = self.red_image\n\n   def run(self, delta):\n      self.step(delta)\n      self.window.clear()\n      self.batch.draw()\n\nworld = World()\n```\n\n# Documentation\n\nhttps://solidsmokesoftware.github.io/pecrs-py/\n\n# Demonstration\n\nhttps://github.com/solidsmokesoftware/solconomy\n\n![solconomy](https://camo.githubusercontent.com/de20b3b2014d20a8746f7346e777e323586d5a35/68747470733a2f2f692e696d6775722e636f6d2f566277677664372e706e67)\n\n# Requirements\n\nTested with Python3.6.9\n',
    'author': 'Solid Smoke Software',
    'author_email': 'solid.smoke.software@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/solidsmokesoftware/pecrs-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)

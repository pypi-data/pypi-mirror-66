from setuptools import setup
import os

name = 'voluptuous-stubs'
description = 'voluptuous stubs'

install_instructions = """\
```
pip install voluptuous-stubs
```
"""


def find_stub_files():
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith('.pyi'):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


setup(name='voluptuous-stubs',
      version='0.1',
      description=description,
      long_description=install_instructions,
      long_description_content_type='text/markdown',
      author='Ryan Wang',
      author_email='hwwangwang@gmail.com',
      license='MIT License',
      url="https://github.com/ryanwang520/voluptuous-stubs",
      install_requires=[
          'mypy>=0.720',
          'typing-extensions>=3.7.4'
      ],
      packages=['voluptuous-stubs'],
      package_data={'voluptuous-stubs': find_stub_files()},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3'
      ]
)

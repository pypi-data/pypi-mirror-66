from os import path
import sys

from setuptools import setup, find_packages

sys.path.insert(0, 'src')
import html5builder


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='html5builder',
    version=html5builder.__version__,
    py_modules=['html5builder'],
    python_requires='>=2.7, !=3.0.*',

    description=html5builder.__doc__,
    url='https://github.com/skitschy/pyHTML5builder',
    author=html5builder.__author__,
    author_email='s1kitschy@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    keywords='html5',
    project_urls={
        'Documentation': 'https://pyhtml5builder.readthedocs.io/',
        'Source': 'https://github.com/skitschy/pyHTML5builder',
    }
)

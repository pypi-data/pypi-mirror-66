# HTML5Builder

HTML5Builder is a Python module
for simply generating strings of HTML5 documents and document fragments.


## Requirement

* Python 2.7 or above


## Installation

```sh
pip install html5builder
```

## Basic Usage

```python
>>> from html5builder import HTML5Builder
>>> tag = HTML5Builder()
>>> img = tag.img(src='image.jpg')
>>> str(img)
'<img src="image.jpg">'
>>> anchor = tag.a([img, 'link'], cls='link', href='target.html')
>>> str(anchor)
'<a href="target.html" class="link"><img src="image.jpg">link</a>'
>>> div = tag.div()
>>> div.child.append(anchor)
>>> str(div)
'<div><a href="target.html" class="link"><img src="image.jpg">link</a></div>'
>>> doc = tag.html([tag.head(''), tag.body('')], lang='ja')
>>> str(tag.doctype + str(doc))
'<!DOCTYPE html><html lang="ja"><head></head><body></body></html>'
```

## Documentation

Documentation is [available online](https://pyhtml5builder.readthedocs.io/).

"""Simple HTML5 document builder."""

__version__ = '0.1.0'
__author__ = 'skitschy'


class HTML5Builder:
    """Simple HTML5 generator class.

    The following code generates a blank japanese HTML5 document.

    >>> tag = HTML5Builder()
    >>> doc = tag.html([tag.head(''), tag.body('')], lang='ja')
    >>> str(tag.doctype + str(doc))
    '<!DOCTYPE html><html lang="ja"><head></head><body></body></html>'
    """

    doctype = '<!DOCTYPE html>'
    """HTML5 Doctype string."""

    class __ElementBuilder(object):
        def __init__(self, name):
            self.name = name

        def __call__(self, children=[], **kwargs):
            if 'cls' in kwargs:
                kwargs['class'] = kwargs.pop('cls')
            return HTML5Element(self.name, children, kwargs)

    def __getattr__(self, name):
        """Return a callable element builder.

        This special method is called
        through ``self.name(children, **kwargs)``.
        This pseudo-method creates a :class:`HTML5Element`.
        The pseudo-method name specifies the name of a generating element.
        The argument ``children`` and the keyword arguments are
        passed to the :class:`HTML5Element` initializer
        as ``children`` and ``attrs`` arguments, respectively.
        In the keyword arguments, ``cls`` can be used instead of ``class``.

        >>> tag = HTML5Builder()
        >>> tag.a('anchor text', href='target.html')
        HTML5Element('a', ['anchor text'], {'href': 'target.html'})
        >>> tag.img(src='image.png')
        HTML5Element('img', [], {'src': 'image.png'})
        >>> tag.div('', cls='divclass')
        HTML5Element('div', [''], {'class': 'divclass'})
        """
        return self.__ElementBuilder(name)


class HTML5Element:
    """Simple HTML5 element class.

    An instance is usually created through :class:`HTML5Builder`.

    Args:
        name (str): The element name.
        children (sequence): The sequence of element children.
        attrs (mapping): The mapping of element attributes.

    If ``children`` is a string or non-sequence,
    the argument is the child of the instance.
    If ``children`` is a sequence,
    the elements of the sequence are the children of the instance.

    Attributes:
        name (str): The element name.
        child (:obj:`list`): The list of element children.
        attrs (:obj:`dict`): The dictionary of element attributes.
    """

    def __init__(self, name, children, attrs):
        self.name = str(name)
        if isinstance(children, str) or not hasattr(children, '__iter__'):
            self.child = [children]
        else:
            self.child = list(children)
        self.attrs = dict(attrs)

    def __getitem__(self, key):
        """Syntax sugar for ``self.attr[key]``."""
        if key in self.attrs:
            return self.attrs[key]
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        """Syntax sugar for ``self.attr[key]=``."""
        self.attrs[key] = value

    def __repr__(self):
        return 'HTML5Element({!r}, {!r}, {!r})'.format(
            self.name, self.child, self.attrs)

    def __str__(self):
        """Output a string of the outer HTML.

        For each child, :func:`str` is recursively called.

        >>> str(HTML5Element('span', 'inner', {}))
        '<span>inner</span>'
        >>> str(HTML5Element('div', '', {'class': 'divclass'}))
        '<div class="divclass"></div>'
        >>> str(HTML5Element('a',
        ...     [HTML5Element('img', [], {'src': 'image.png'}), 'anchor text'],
        ...     {'href': 'target.html'}))
        '<a href="target.html"><img src="image.png">anchor text</a>'
        """
        if self.attrs:
            attrstr = ' '.join(
                [''] + ['{}="{}"'.format(k, v) for k, v in self.attrs.items()])
        else:
            attrstr = ''
        if self.child:
            inner = ''.join([str(child) for child in self.child])
            return '<{0}{1}>{2}</{0}>'.format(self.name, attrstr, inner)
        else:
            return '<{0}{1}>'.format(self.name, attrstr)

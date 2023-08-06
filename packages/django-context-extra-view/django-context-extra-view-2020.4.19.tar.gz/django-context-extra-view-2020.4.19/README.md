<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-context-extra-view.svg?longCache=True)](https://pypi.org/project/django-context-extra-view/)
[![](https://img.shields.io/pypi/v/django-context-extra-view.svg?maxAge=3600)](https://pypi.org/project/django-context-extra-view/)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![Travis](https://api.travis-ci.org/andrewp-as-is/django-context-extra-view.py.svg?branch=master)](https://travis-ci.org/andrewp-as-is/django-context-extra-view.py/)

#### Installation
```bash
$ [sudo] pip install django-context-extra-view
```

#### Examples
```python
from django_context_extra_view.views import ContextExtraViewMixin

class View(ContextExtraViewMixin,...):
    context_extra = {"my_page":{"active":True}}
```

```html
{% if my_page.active %}...{% endif %}
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>
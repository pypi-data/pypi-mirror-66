# django-static-jquery3


Django application contain jquery and jquery-plugins' static files.


## Install

```shell
pip install django-static-jquery3
```

## Installed Plugins

- jquery.cookie.js

## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    "django_static_jquery3",
    ...
]
```

**app/template/app/index.html**

```html
{% load static %}

<script src="{% static "jquery3/jquery.js" %}"></script>
<script src="{% static "jquery3/plugins/jquery.cookie.js" %}"></script>
```

## About releases

1. The first three number is the same with jquery project's version.
1. The fourth number is our release number, it's optional.

## Releases

### v3.4.1.1 2020/04/23

- Add jquery plugin: jquery.cookie.
- Fix document.

### v3.4.1.0 2020/04/10

- Upgrade jquery to 3.4.1.

### v3.3.1.1 2018/03/27

- Upgrade jquery to 3.3.1.

## v3.2.1 2017/12/23

- First release with jquery 3.2.1.

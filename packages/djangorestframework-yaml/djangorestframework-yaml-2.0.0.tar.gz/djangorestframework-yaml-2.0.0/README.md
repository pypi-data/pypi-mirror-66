# REST Framework YAML

[![build-status-image]][github-action]
[![pypi-version]][pypi]

**YAML support for Django REST Framework**

Full documentation for the project is available at [http://jpadilla.github.io/django-rest-framework-yaml][docs].

## Overview

YAML support extracted as a third party package directly from the official Django REST Framework implementation. It's built using the [PyYAML][pyyaml] package.

## Requirements

* Python (2.7, 3.3, 3.4)
* Django (1.6, 1.7)

## Installation

Install using `pip`...

```bash
$ pip install djangorestframework-yaml
```

## Example

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_yaml.parsers.YAMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_yaml.renderers.YAMLRenderer',
    ),
}
```

You can also set the renderer and parser used for an individual view, or viewset, using the APIView class based views.

```python
from rest_framework import routers, serializers, viewsets
from rest_framework_yaml.parsers import YAMLParser
from rest_framework_yaml.renderers import YAMLRenderer

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)
```

### Sample output

```yaml
---
-
  email: jpadilla@example.com
  is_staff: true
  url: "http://127.0.0.1:8000/users/1/"
  username: jpadilla
```

## Documentation & Support

Full documentation for the project is available at [http://jpadilla.github.io/django-rest-framework-yaml][docs].

You may also want to follow the [author][jpadilla] on Twitter.


[build-status-image]: https://github.com/jpadilla/django-rest-framework-yaml/workflows/CI/badge.svg
[github-action]: https://github.com/jpadilla/django-rest-framework-yaml/actions?query=workflow%3ACI
[pypi-version]: https://img.shields.io/pypi/v/djangorestframework-yaml.svg
[pypi]: https://pypi.python.org/pypi/djangorestframework-yaml
[pyyaml]: http://pyyaml.org/
[docs]: http://jpadilla.github.io/django-rest-framework-yaml
[jpadilla]: https://twitter.com/jpadilla_

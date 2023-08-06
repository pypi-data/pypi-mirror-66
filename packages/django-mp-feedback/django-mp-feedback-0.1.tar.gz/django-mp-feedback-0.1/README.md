
Django feedback app.

### Installation

Install with pip:

```
pip install django-mp-feedback
```

Settings:
```
INSTALLED_APPS = [
    ...,
    'feedback'
]
```

Urls:
```
path('feedback/', include('feedback.urls')),
```

Using:
```
{% load feedback %}

{% block js %}

    ...

    {% feedback_form_js %}

{% endblock %}
```

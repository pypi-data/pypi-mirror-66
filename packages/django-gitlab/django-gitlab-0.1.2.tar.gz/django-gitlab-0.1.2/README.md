# Django GitLab

### Documentation


### Streamlined Installation and Configuration

Create a new project in GitLab using the Django GitLab Template.

### Manual Installation

```bash
pip install django-gitlab
```

### Manual Configuration

`setup.py`

```python
UNLEASH_API_URL = ''
UNLEASH_API_IID = ''
UNLEASH_APP_NAME = ''
UNLEASH_ENVIRONMENT = ''
if UNLEASH_API_URL:
    try:
        from UnleashClient import UnleashClient
        UNLEASH = UnleashClient(
            url=UNLEASH_API_URL,
            app_name=UNLEASH_APP_NAME,
            environment=UNLEASH_ENVIRONMENT,
            disable_metrics=True,
            disable_registration=True,
        )
    except ImportError:
        UNLEASH = None


SENTRY_DSN = ''
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
```

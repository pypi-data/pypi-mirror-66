# Django GitLab

Make GitLab your complete DevOps platform delivered as a single application

* [x]  Containerized App in Kubernetes
* [x]  Security Scans
* [x]  Error Tracking
* [x]  Feature Flags

### Documentation


### Streamlined Installation and Configuration

Create a new project in GitLab using the Django GitLab Template.

### Manual Installation

```bash
pip install django-gitlab
```

### Manual Configuration

`settings.py`

```python
# Placed at the very end of your settings file:
from django_gitlab import conf
conf.settings(locals())
```

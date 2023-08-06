# Django GitLab

Make GitLab your complete DevOps platform delivered as a single application

* [x]  Containerized App in Kubernetes
* [x]  Security Scans
* [x]  Error Tracking
* [x]  Feature Flags

### Documentation


### Streamlined Installation and Configuration

Create a new project in GitLab using the Django GitLab Template.


**Step 1.**

Add `django_gitlab` to your `requirements.txt` file.

**Step 2.**
```yaml
include:
  remote: https://gitlab.com/poffey21/django-gitlab/-/raw/master/Django.gitlab-ci.yml
```

**Step 3.**

Install on workstation and follow instructions.

```bash
> pip install django-gitlab[cli]
> python manage.py gitlab
```

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

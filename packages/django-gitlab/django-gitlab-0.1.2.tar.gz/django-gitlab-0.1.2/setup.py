from setuptools import setup

import django_gitlab

setup(
    name="django-gitlab",
    version=django_gitlab.__version__,
    description="Simple integration for GitLab and Django",
    long_description="Provides users an easy way to get started with GitLab and Django",
    keywords="django, gitlab, unleash, feature flags, sentry, error tracking",
    author="Tim Poffenbarger <poffey21@gmail.com>",
    author_email="poffey21@gmail.com",
    url="https://gitlab.com/poffey21/django-gitlab/",
    license="BSD",
    packages=["django_gitlab"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0"
    ],
    install_requires=[
        "Django>=1.11.0",
        "UnleashClient>=3.4.0",
        "sentry-sdk>=0.14.0"
    ],
)

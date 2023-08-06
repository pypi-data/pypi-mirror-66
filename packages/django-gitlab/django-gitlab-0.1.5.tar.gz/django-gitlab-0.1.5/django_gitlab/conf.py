import logging
import os
from environ import Env

logger = logging.getLogger(__name__)


# SECURITY WARNING: keep the secret key used in production secret!
def gen_sec_key():
    try:
        import random
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        length = 50
        return ''.join(chars[random.randint(0, len(chars) - 1)] for i in range(length))
    except (IndexError, RuntimeError, RecursionError):
        return 'unsafeunsafeunsafeunsafe'


def settings(config, *,
             debug=True, databases=True, sentry=True, unleash=True,
             staticfiles=True, allowed_hosts=True, logging=True, secret_key=True,
             context_processors=True, installed_apps=True,
             ):

    env = Env()
    if 'BASE_DIR' in config and os.path.isfile(os.path.join(config['BASE_DIR'], 'www/.env')):
        env.read_env()

    if context_processors:
        try:
            processors = [
                'django_gitlab.context_processors.feature_flags',
                'django_gitlab.context_processors.gitlab_links',
            ]
            if not any(x in config['TEMPLATES'][0]['OPTIONS']['context_processors'] for x in processors):
                config['TEMPLATES'][0]['OPTIONS']['context_processors'].extend(processors)
        except (IndexError, KeyError):
            pass

    # Install App
    if installed_apps:
        if 'django_gitlab' not in config['INSTALLED_APPS']:
            config['INSTALLED_APPS'] = tuple(
                list(config['INSTALLED_APPS']) + ['django_gitlab']
            )

    # Database configuration.
    if databases:
        # Integrity check.
        if 'DATABASES' not in config:
            config['DATABASES'] = {'default': None}

        config['DATABASES']['default'] = env.db(default='sqlite:///db.sqlite3')

    # Staticfiles configuration.
    if staticfiles:
        logger.info('Applying GitLab Staticfiles configuration to Django settings.')

        config['STATIC_ROOT'] = os.path.join(config['BASE_DIR'], 'static')
        config['STATIC_URL'] = '/static/'

        # Ensure STATIC_ROOT exists.
        os.makedirs(config['STATIC_ROOT'], exist_ok=True)

        # Insert Whitenoise Middleware.
        try:
            config['MIDDLEWARE_CLASSES'] = tuple(
                ['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE_CLASSES'])
            )
        except KeyError:
            config['MIDDLEWARE'] = tuple(['whitenoise.middleware.WhiteNoiseMiddleware'] + list(config['MIDDLEWARE']))

        # Enable GZip.
        config['STATICFILES_STORAGE'] = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    if allowed_hosts:
        logger.info('Applying GitLab ALLOWED_HOSTS configuration to Django settings.')
        config['ALLOWED_HOSTS'] = ['*']

    if logging:
        logger.info('Applying GitLab logging configuration to Django settings.')

        config['LOGGING'] = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                               'pathname=%(pathname)s lineno=%(lineno)s ' +
                               'funcname=%(funcName)s %(message)s'),
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'simple': {
                    'format': '%(levelname)s %(message)s'
                }
            },
            'handlers': {
                'null': {
                    'level': 'DEBUG',
                    'class': 'logging.NullHandler',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                }
            },
            'loggers': {
                'testlogger': {
                    'handlers': ['console'],
                    'level': 'INFO',
                }
            }
        }

    if secret_key:
        # SECRET_KEY configuration.
        try:
            config['SECRET_KEY'] = env('SECRET_KEY', default=gen_sec_key())
        except RecursionError:
            config['SECRET_KEY'] = gen_sec_key()

    if debug:
        config['DEBUG'] = env('DEBUG', cast=bool, default=False, )

    if sentry:
        SENTRY_DSN = env('SENTRY_DSN', default='')
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

    if unleash:
        # from django.conf import settings; from UnleashClient import UnleashClient; c = UnleashClient(settings.UNLEASH_API_URL, settings.UNLEASH_API_IID); c.initialize_client();
        url = env('UNLEASH_API_URL', default='')
        instance_id = env('UNLEASH_API_IID', default='')
        app_name = env('UNLEASH_API_NAME', default='')
        if url:
            try:
                from UnleashClient import UnleashClient
                config['UNLEASH'] = UnleashClient(
                    url=url,
                    app_name=app_name,
                    environment=env('GITLAB_ENVIRONMENT_NAME', default='dev'),
                    instance_id=instance_id,
                    disable_metrics=True,
                    disable_registration=True
                )
            except ImportError:
                config['UNLEASH'] = None

    # locals()['GITLAB_BLAH'] = 'hello'
    config['GITLAB_PROJECT_URL'] = env('GITLAB_PROJECT_URL', default='')
    config['GITLAB_COMMIT_SHA'] = env('GITLAB_COMMIT_SHA', default='')
    config['GITLAB_COMMIT_SHORT_SHA'] = env('GITLAB_COMMIT_SHORT_SHA', default='')
    config['GITLAB_SERVER_VERSION'] = env('GITLAB_SERVER_VERSION', default='')
    config['GITLAB_RUNNER_VERSION'] = env('GITLAB_RUNNER_VERSION', default='')
    config['GITLAB_ENVIRONMENT_NAME'] = env('GITLAB_ENVIRONMENT_NAME', default='')

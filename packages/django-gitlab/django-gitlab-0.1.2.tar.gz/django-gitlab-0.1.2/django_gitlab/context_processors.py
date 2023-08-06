from logging import getLogger
from . import services
from django.conf import settings

logger = getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def feature_flags(request):
    features = {
        'feature': {},
    }
    context = {}
    if request.user.is_authenticated:
        context['userId'] = request.user.username
    c = services.get_feature_flag_service()
    features['feature'] = {
        x: c.is_enabled(x, context=context)
        for x in c.features.keys()
    }
    return features


def gitlab_links(request):
    if not hasattr(settings, 'GITLAB_PROJECT_URL') or not settings.GITLAB_PROJECT_URL:
        return {
            'gitlab': {
                'feature_flags_url': '#',
                'error_tracking_url': '#',
            }
        }

    links = {
        'gitlab': {
            'project_url': settings.GITLAB_PROJECT_URL,
            'feature_flags_url': settings.GITLAB_PROJECT_URL + '/-/feature_flags',
            'error_tracking_url': settings.GITLAB_PROJECT_URL + '/-/error_tracking',
            'commit_short_sha': settings.GITLAB_COMMIT_SHORT_SHA,
            'commit_sha': settings.GITLAB_COMMIT_SHA,
            'runner_version': settings.GITLAB_RUNNER_VERSION,
            'server_version': settings.GITLAB_SERVER_VERSION,
            'environment_name': settings.GITLAB_ENVIRONMENT_NAME,
            'client_ip': get_client_ip(request),
        }
    }
    return links

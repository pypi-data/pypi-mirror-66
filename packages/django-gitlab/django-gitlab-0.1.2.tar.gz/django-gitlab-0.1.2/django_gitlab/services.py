from logging import getLogger

from django.conf import settings

logger = getLogger(__name__)


def get_feature_flag_service():
    if "client" not in get_feature_flag_service.__dict__:
        logger.debug("Creating Feature Flag service")
        get_feature_flag_service.client = settings.UNLEASH
        logger.debug("Created Feature Flag service")
    else:
        logger.debug("Returning existing Feature Flag Service")

    if not get_feature_flag_service.client.is_initialized:
        logger.debug("Initializing Feature Flag Client")
        get_feature_flag_service.client.initialize_client()
        logger.debug("Feature Flag Client is now initialized")
    else:
        logger.debug("Feature Flag Client had already been initialized")

    return get_feature_flag_service.client

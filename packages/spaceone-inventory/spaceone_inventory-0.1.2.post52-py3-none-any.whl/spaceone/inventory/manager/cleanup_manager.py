import logging

from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger(__name__)


class CleanupManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_domains(self, query):
        identity_connector = self.locator.get_connector('IdentityConnector')
        return identity_connector.list_domains(query)


from spaceone.core.service import *
from spaceone.inventory.manager.cleanup_manager import CleanupManager


@authentication_handler
@authorization_handler
@event_handler
class CleanupService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @append_query_filter([])
    def list_domains(self, params):
        """
        Returns:
            results (list)
            total_count (int)
        """
        mgr = self.locator.get_manager('CleanupManager')
        query = params.get('query', {})
        result = mgr.list_domains(query)
        return result

    @transaction
    @check_required(['domain_id'])
    def cleanup(self, params):
        """
        Args:
            params (dict): {
            }

        Returns:
            values (list) : 'list of statistics data'

        """
        print('=' * 30)
        print(params)

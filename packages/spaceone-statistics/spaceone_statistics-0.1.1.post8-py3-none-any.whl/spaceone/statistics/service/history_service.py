import logging

from spaceone.core.service import *
from spaceone.statistics.error import *
from spaceone.statistics.manager.resource_manager import ResourceManager
from spaceone.statistics.manager.history_manager import HistoryManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class HistoryService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource_mgr: ResourceManager = self.locator.get_manager('ResourceManager')
        self.history_mgr: HistoryManager = self.locator.get_manager('HistoryManager')

    @transaction
    @check_required(['topic', 'resource_type', 'query', 'domain_id'])
    def create(self, params):
        """Statistics query to resource

        Args:
            params (dict): {
                'topic': 'str',
                'data_source_id': 'str',
                'resource_type': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)',
                'join': 'list',
                'formulas': 'list',
                'domain_id': 'str'
            }

        Returns:
            None
        """

        domain_id = params['domain_id']
        resource_type = params['resource_type']
        query = params.get('query', {})
        join = params.get('join', [])
        formulas = params.get('formulas', [])
        sort = query.get('sort')
        limit = query.get('limit')

        if len(join) > 0:
            query['sort'] = None
            query['limit'] = None

        results = self.resource_mgr.stat(resource_type, query, domain_id)
        params['results'] = self.resource_mgr.join_and_execute_formula(results, resource_type, query, join, formulas,
                                                                       sort, limit, domain_id)

        self.history_mgr.create_history(params)

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['topic', 'domain_id'])
    @append_keyword_filter(['topic'])
    @change_timestamp_filter(['created_at'])
    def list(self, params):
        """ List history

        Args:
            params (dict): {
                'topic': 'str',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)'
            }

        Returns:
            history_vos (object)
            total_count
        """

        query = params.get('query', {})
        return self.history_mgr.list_history(query)

    @transaction
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    @change_timestamp_filter(['created_at'])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get('query', {})
        return self.history_mgr.stat_history(query)

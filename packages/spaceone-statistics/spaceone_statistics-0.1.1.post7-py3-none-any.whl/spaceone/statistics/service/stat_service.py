import logging

from spaceone.core.service import *

from spaceone.statistics.error import *
from spaceone.statistics.manager.stat_manager import StatManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class StatService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stat_mgr: StatManager = self.locator.get_manager('StatManager')

    @transaction
    @check_required(['resource_type', 'query', 'domain_id'])
    def query(self, params):
        """Statistics query to resource

        Args:
            params (dict): {
                'data_source_id': 'str',
                'resource_type': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)',
                'join': 'list',
                'formulas': 'list',
                'domain_id': 'str'
            }

        Returns:
            stat_info (object)
        """
        domain_id = params['domain_id']
        resource_type = params['resource_type']
        query = params.get('query', {})
        join = params.get('join', [])
        formulas = params.get('formulas', [])
        sort = query.get('sort')
        limit = query.get('limit')

        if len(join) > 0 or len(formulas) > 0:
            query['sort'] = None
            query['limit'] = None

        results = self.stat_mgr.query(resource_type, query, domain_id)
        results = self.stat_mgr.join_and_execute_formula(results, resource_type, query, join,
                                                         formulas, sort, limit, domain_id)

        return {
            'resource_type': resource_type,
            'results': results,
            'domain_id': domain_id
        }

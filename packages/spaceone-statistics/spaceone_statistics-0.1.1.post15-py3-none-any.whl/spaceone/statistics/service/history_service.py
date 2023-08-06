import logging
from datetime import datetime

from spaceone.core.service import *
from spaceone.statistics.error import *
from spaceone.statistics.manager.resource_manager import ResourceManager
from spaceone.statistics.manager.schedule_manager import ScheduleManager
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
    @check_required(['schedule_id', 'resource_type', 'query', 'domain_id'])
    def create(self, params):
        """Statistics query to resource

        Args:
            params (dict): {
                'schedule_id': 'str',
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

        schedule_mgr: ScheduleManager = self.locator.get_manager('ScheduleManager')

        domain_id = params['domain_id']
        schedule_id = params['schedule_id']
        resource_type = params['resource_type']
        query = params.get('query', {})
        join = params.get('join', [])
        formulas = params.get('formulas', [])
        sort = query.get('sort')
        limit = query.get('limit')

        schedule_vo = schedule_mgr.get_schedule(schedule_id, domain_id, ['schedule_id', 'topic'])

        params['schedule'] = schedule_vo
        params['topic'] = schedule_vo.topic

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

    @transaction
    @check_required(['topic', 'start', 'end', 'default_fields', 'diff_fields', 'domain_id'])
    @change_timestamp_value(['start', 'end'], timestamp_format='iso8601')
    def diff(self, params):
        """
        Args:
            params (dict): {
                'start': 'timestamp',
                'end': 'timestamp',
                'default_fields': 'list',
                'diff_fields': 'list',
                'domain_id': 'str'
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        domain_id = params['domain_id']
        topic = params['topic']
        start = params['start']
        end = params['end']
        default_fields = params['default_fields']
        diff_fields = params['diff_fields']

        query = self._make_statistics_query(topic, start, end, domain_id)

        results = self.history_mgr.stat_history(query)
        _LOGGER.debug(f'[diff] stat results: {results}')
        first_data, last_data = self._get_first_and_last_results(results, start, end)
        return self.history_mgr.diff_history(first_data, last_data, default_fields, diff_fields)

    @staticmethod
    def _get_first_and_last_results(results, start: datetime, end: datetime):
        if len(results) <= 1:
            raise ERROR_DIFF_TIME_RANGE(start=f'{start.isoformat()}Z', end=f'{end.isoformat()}Z')

        return results[0]['data'], results[-1:][0]['data']

    @staticmethod
    def _make_statistics_query(topic, start, end, domain_id):
        _query = {
            'filter': [{
                'k': 'topic',
                'v': topic,
                'o': 'eq'
            }, {
                'k': 'domain_id',
                'v': domain_id,
                'o': 'eq'
            }, {
                'k': 'created_at',
                'v': start,
                'o': 'gte'
            }, {
                'k': 'created_at',
                'v': end,
                'o': 'lte'
            }],
            'aggregate': {
                'group': {
                    'keys': [{
                        'k': 'created_at',
                        'n': 'created_at'
                    }],
                    'fields': [{
                        'k': 'values',
                        'o': 'add_to_set',
                        'n': 'data'
                    }]
                }
            },
            'sort': {
                'name': 'created_at'
            }
        }

        return _query

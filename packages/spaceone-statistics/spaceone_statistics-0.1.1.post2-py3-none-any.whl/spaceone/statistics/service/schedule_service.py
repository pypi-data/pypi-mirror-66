import logging

from spaceone.core.service import *

from spaceone.statistics.error import *
from spaceone.statistics.manager.stat_manager import StatManager
from spaceone.statistics.manager.schedule_manager import ScheduleManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class ScheduleService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stat_mgr: StatManager = self.locator.get_manager('StatManager')
        self.schedule_mgr: ScheduleManager = self.locator.get_manager('ScheduleManager')

    @transaction
    @check_required(['topic', 'option', 'schedule', 'domain_id'])
    def add(self, params):
        """Statistics query to resource

        Args:
            params (dict): {
                'topic': 'str',
                'option': 'dict',
                'schedule': 'dict',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            schedule_vo
        """

        domain_id = params['domain_id']
        option = params['option']
        schedule = params['schedule']

        self._check_schedule(schedule)
        self._verify_query_option(option, domain_id)

        return self.schedule_mgr.add_schedule(params)

    @transaction
    @check_required(['schedule_id', 'domain_id'])
    def update(self, params):
        """Add schedule for statistics

        Args:
            params (dict): {
                'schedule_id': 'str',
                'schedule': 'dict',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            schedule_vo
        """
        schedule = params.get('schedule')

        self._check_schedule(schedule)

        return self.schedule_mgr.update_schedule(params)

    @transaction
    @check_required(['schedule_id', 'domain_id'])
    def enable(self, params):
        """Enable schedule

        Args:
            params (dict): {
                'schedule_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            schedule_vo
        """

        domain_id = params['domain_id']
        schedule_id = params['schedule_id']

        schedule_vo = self.schedule_mgr.get_schedule(schedule_id, domain_id)
        return self.schedule_mgr.update_schedule_by_vo({'state': 'ENABLED'}, schedule_vo)

    @transaction
    @check_required(['schedule_id', 'domain_id'])
    def disable(self, params):
        """Disable schedule

        Args:
            params (dict): {
                'schedule_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            schedule_vo
        """

        domain_id = params['domain_id']
        schedule_id = params['schedule_id']

        schedule_vo = self.schedule_mgr.get_schedule(schedule_id, domain_id)
        return self.schedule_mgr.update_schedule_by_vo({'state': 'DISABLED'}, schedule_vo)

    @transaction
    @check_required(['schedule_id', 'domain_id'])
    def delete(self, params):
        """Delete schedule

        Args:
            params (dict): {
                'schedule_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            None
        """

        self.schedule_mgr.delete_schedule(params['schedule_id'], params['domain_id'])

    @transaction
    @check_required(['schedule_id', 'domain_id'])
    def get(self, params):
        """Get schedule

        Args:
            params (dict): {
                'schedule_id': 'str',
                'domain_id': 'str',
                'only': 'list'
            }

        Returns:
            schedule_vo
        """

        return self.schedule_mgr.get_schedule(params['schedule_id'], params['domain_id'], params.get('only'))

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['schedule_id', 'topic', 'state', 'data_source_id', 'resource_type', 'domain_id'])
    @append_keyword_filter(['schedule_id', 'topic', 'resource_type'])
    @change_timestamp_filter(['created_at', 'last_scheduled_at'])
    def list(self, params):
        """ List schedules

        Args:
            params (dict): {
                'schedule_id': 'str',
                'topic': 'str',
                'state': 'str',
                'data_source_id': 'str',
                'resource_type': 'str',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)'
            }

        Returns:
            schedule_vos (object)
            total_count
        """

        query = params.get('query', {})
        return self.schedule_mgr.list_schedules(query)

    @transaction
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    @change_timestamp_filter(['created_at', 'last_scheduled_at'])
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
        return self.schedule_mgr.stat_schedules(query)

    @staticmethod
    def _check_schedule(schedule):
        if schedule and len(schedule) > 1:
            raise ERROR_SCHEDULE_OPTION()

    @staticmethod
    def _check_query_option(option):
        if 'resource_type' not in option:
            raise ERROR_REQUIRED_PARAMETER(key='option.resource_type')

        if 'query' not in option:
            raise ERROR_REQUIRED_PARAMETER(key='option.query')

    def _verify_query_option(self, option, domain_id):
        self._check_query_option(option)

        resource_type = option['resource_type']
        query = option['query']
        join = option.get('join', [])
        formulas = option.get('formulas', [])
        sort = query.get('sort')
        limit = query.get('limit')

        if len(join) > 0:
            query['sort'] = None
            query['limit'] = None

        results = self.stat_mgr.query(resource_type, query, domain_id)
        self.stat_mgr.join_and_execute_formula(results, join, formulas, sort, limit, domain_id)

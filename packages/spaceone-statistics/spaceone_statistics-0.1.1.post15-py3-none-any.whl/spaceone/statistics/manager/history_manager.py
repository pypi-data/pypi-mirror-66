import logging
import pandas as pd
from datetime import datetime

from spaceone.core.manager import BaseManager
from spaceone.statistics.error import *
from spaceone.statistics.model.history_model import History

_LOGGER = logging.getLogger(__name__)


class HistoryManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history_model: History = self.locator.get_model('History')

    def create_history(self, params):
        def _rollback(history_vo):
            _LOGGER.info(f'[create_history._rollback] '
                         f'Delete history : {history_vo.topic}')
            history_vo.delete()

        created_at = datetime.utcnow()

        for values in params['results']:
            history_data = {
                'topic': params['topic'],
                'schedule': params['schedule'],
                'values': values,
                'created_at': created_at,
                'domain_id': params['domain_id']
            }

            _LOGGER.debug(f'[create_history] create history: {history_data}')

            history_vo: History = self.history_model.create(history_data)

            self.transaction.add_rollback(_rollback, history_vo)

    def list_history(self, query={}):
        return self.history_model.query(**query)

    def stat_history(self, query):
        return self.history_model.stat(**query)

    def diff_history(self, before_data, after_data, default_fields, diff_fields):
        before_df = pd.DataFrame(before_data)
        after_df = pd.DataFrame(after_data)

        _LOGGER.debug(f'[before data frame] >>\n{before_df}')
        _LOGGER.debug(f'[after data frame] >>\n{after_df}')

        joined_df = self._join_history(before_df, after_df, default_fields)
        diff_df = self._diff_history(joined_df, diff_fields)

        results = self._make_results(diff_df, default_fields, diff_fields)
        return results

    @staticmethod
    def _make_results(diff_df, default_fields, diff_fields):
        results = []
        for row in diff_df.to_dict('records'):
            values = {}
            for field in default_fields:
                values[field] = row[f'{field}_default']

            for field in diff_fields:
                values[field] = row[f'{field}_after_diff']

            results.append(values)

        final_df = pd.DataFrame(results)
        _LOGGER.debug(f'[final data frame]>>\n{final_df}')

        return results

    @staticmethod
    def _diff_history(joined_df, diff_fields):
        diff_df = joined_df.diff(axis=1, periods=len(diff_fields))
        diff_df = joined_df.merge(diff_df, right_index=True, left_index=True, suffixes=('_default', '_diff'))
        _LOGGER.debug(f'[diff data frame]>>\n{diff_df}')

        return diff_df

    @staticmethod
    def _join_history(before_df, after_df, default_fields):
        joined_df = before_df.merge(after_df, how='outer', on=default_fields, suffixes=('_before', '_after'))
        joined_df = joined_df.fillna(0)
        _LOGGER.debug(f'[joined data frame]>>\n{joined_df}')

        return joined_df

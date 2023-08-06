import functools
from spaceone.api.statistics.v1 import schedule_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.statistics.model.schedule_model import Schedule, Scheduled, JoinQuery, Formula, QueryOption

__all__ = ['ScheduleInfo', 'SchedulesInfo']


def ScheduledInfo(vo: Scheduled):
    info = {
        'cron': vo.cron,
        'interval': vo.interval,
        'hours': vo.hours,
        'minutes': vo.minutes
    }
    return schedule_pb2.Scheduled(**info)


def JoinQueryInfo(vo: JoinQuery):
    info = {
        'key': vo.key,
        'data_source_id': vo.data_source_id,
        'resource_type': vo.resource_type,
        'query': change_stat_query(vo.query)
    }
    return schedule_pb2.ScheduleJoinQuery(**info)


def FormulaInfo(vo: Formula):
    info = {
        'name': vo.name,
        'formula': vo.formula
    }
    return schedule_pb2.ScheduleFormula(**info)


def QueryOptionInfo(vo: QueryOption):
    info = {
        'data_source_id': vo.data_source_id,
        'resource_type': vo.resource_type,
        'query': change_stat_query(vo.query),
        'join': list(map(JoinQueryInfo, vo.join)) if vo.join else None,
        'formulas': list(map(FormulaInfo, vo.formulas)) if vo.formulas else None,
    }
    return schedule_pb2.QueryOption(**info)


def ScheduleInfo(schedule_vo: Schedule, minimal=False):
    info = {
        'schedule_id': schedule_vo.schedule_id,
        'topic': schedule_vo.topic,
        'state': schedule_vo.state,
    }

    if not minimal:
        info.update({
            'options': QueryOptionInfo(schedule_vo.options) if schedule_vo.options else None,
            'schedule': ScheduledInfo(schedule_vo.schedule) if schedule_vo.schedule else None,
            'tags': change_struct_type(schedule_vo.tags),
            'domain_id': schedule_vo.domain_id,
            'created_at': change_timestamp_type(schedule_vo.created_at),
            'last_scheduled_at': change_timestamp_type(schedule_vo.last_scheduled_at)
        })

    return schedule_pb2.ScheduleInfo(**info)


def SchedulesInfo(schedule_vos, total_count, **kwargs):
    return schedule_pb2.SchedulesInfo(results=list(
        map(functools.partial(ScheduleInfo, **kwargs), schedule_vos)), total_count=total_count)

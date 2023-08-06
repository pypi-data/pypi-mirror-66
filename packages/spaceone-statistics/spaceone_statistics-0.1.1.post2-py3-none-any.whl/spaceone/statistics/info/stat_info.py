from spaceone.api.statistics.v1 import stat_pb2
from spaceone.core.pygrpc.message_type import *

__all__ = ['StatInfo']


def StatInfo(stat_info):
    info = {
        'results': change_list_value_type(stat_info.get('results', [])),
        'domain_id': stat_info['domain_id']
    }

    return stat_pb2.StatInfo(**info)

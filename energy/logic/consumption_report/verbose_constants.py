from django.utils.translation import gettext as _

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import OneHourAggregationIntervalQueryParameters


def get_aggregation_interval_verbose(interval: AggregationIntervalSeconds) -> str:
    __AGGREGATION_INTERVALS_VERBOSE = {
        AggregationIntervalSeconds.ONE_HOUR:  _('година'),
        AggregationIntervalSeconds.ONE_DAY:   _('доба'),
        AggregationIntervalSeconds.ONE_WEEK:  _('тиждень'),
        AggregationIntervalSeconds.ONE_MONTH: _('місяць'),
        AggregationIntervalSeconds.ONE_YEAR:  _('рік'),
    }
    return __AGGREGATION_INTERVALS_VERBOSE[interval]


def get_hour_filtering_method_verbose(
        hour_filtering_method: OneHourAggregationIntervalQueryParameters.HourFilteringMethods
) -> str:
    __ = OneHourAggregationIntervalQueryParameters.HourFilteringMethods
    __HOUR_FILTERING_METHODS_VERBOSE = {
        __.EVERY_DAY:      _('кожен день'),
        __.WHOLE_INTERVAL: _('увесь інтервал'),
    }
    return __HOUR_FILTERING_METHODS_VERBOSE[hour_filtering_method]

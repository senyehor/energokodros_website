from django.utils.translation import gettext as _

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds

__AGGREGATION_INTERVALS_VERBOSE = {
    AggregationIntervalSeconds.ONE_HOUR:  _('година'),
    AggregationIntervalSeconds.ONE_DAY:   _('доба'),
    AggregationIntervalSeconds.ONE_WEEK:  _('тиждень'),
    AggregationIntervalSeconds.ONE_MONTH: _('місяць'),
    AggregationIntervalSeconds.ONE_YEAR:  _('рік'),
}


def get_aggregation_interval_verbose(interval: AggregationIntervalSeconds) -> str:
    return __AGGREGATION_INTERVALS_VERBOSE[interval]

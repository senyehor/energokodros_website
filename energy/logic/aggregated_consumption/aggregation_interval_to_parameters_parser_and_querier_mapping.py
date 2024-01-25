from typing import Type

from energy.logic.aggregated_consumption.aggregated_consumption_queriers import (
    AnyQuerier, OneDayQuerier, OneHourQuerier,
    OneMonthQuerier, OneWeekQuerier, OneYearQuerier,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters_parsers import (
    AnyParametersParser, CommonQueryParametersParser,
    OneDayAggregationIntervalQueryParametersParser,
    OneHourAggregationIntervalQueryParametersParser,
)

__DEFAULT_QUERY_PARAMETERS_PARSER = CommonQueryParametersParser

AnyParserTypeWithAnyQuerierType = tuple[Type[AnyParametersParser], Type[AnyQuerier]]
AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_AND_QUERIER_MAPPING: \
    dict[
        AggregationIntervalSeconds,
        AnyParserTypeWithAnyQuerierType
    ] = \
    {
        AggregationIntervalSeconds.ONE_HOUR:  (
            OneHourAggregationIntervalQueryParametersParser,
            OneHourQuerier
        ),
        AggregationIntervalSeconds.ONE_DAY:   (
            OneDayAggregationIntervalQueryParametersParser,
            OneDayQuerier
        ),
        AggregationIntervalSeconds.ONE_WEEK:  (
            __DEFAULT_QUERY_PARAMETERS_PARSER,
            OneWeekQuerier
        ),
        AggregationIntervalSeconds.ONE_MONTH: (
            __DEFAULT_QUERY_PARAMETERS_PARSER,
            OneMonthQuerier
        ),
        AggregationIntervalSeconds.ONE_YEAR:  (
            __DEFAULT_QUERY_PARAMETERS_PARSER,
            OneYearQuerier
        ),
    }


def get_parser_and_querier_for_interval(interval: AggregationIntervalSeconds) \
        -> AnyParserTypeWithAnyQuerierType:
    return AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_AND_QUERIER_MAPPING[interval]

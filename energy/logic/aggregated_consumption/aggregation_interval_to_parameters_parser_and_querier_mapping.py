from typing import TypeAlias

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters_parsers import (
    AnyParametersParser,
    CommonPostQueryParametersParser, OneHourAggregationIntervalPostQueryParametersParser,
)
from energy.logic.aggregated_consumption.queriers import (
    AnyQuerier, OneDayQuerier, OneHourQuerier,
    OneMonthQuerier, OneWeekQuerier, OneYearQuerier,
)

__DEFAULT_QUERY_PARAMETERS_PARSER = CommonPostQueryParametersParser

ParserAndQuerier: TypeAlias = tuple[AnyParametersParser, AnyQuerier]

AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_AND_QUERIER_MAPPING: \
    dict[
        AggregationIntervalSeconds,
        ParserAndQuerier
    ] = \
    {
        AggregationIntervalSeconds.ONE_HOUR:  (
            OneHourAggregationIntervalPostQueryParametersParser,
            OneHourQuerier
        ),
        AggregationIntervalSeconds.ONE_DAY:   (
            __DEFAULT_QUERY_PARAMETERS_PARSER,
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

from typing import Type

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters_parsers import (
    AnyParametersParser,
    CommonPostQueryParametersParser, OneDayAggregationIntervalPostQueryParametersParser,
    OneHourAggregationIntervalPostQueryParametersParser,
)
from energy.logic.aggregated_consumption.queriers import (
    AnyQuerier, OneDayQuerier, OneHourQuerier,
    OneMonthQuerier, OneWeekQuerier, OneYearQuerier,
)

__DEFAULT_QUERY_PARAMETERS_PARSER = CommonPostQueryParametersParser

ParserAndQuerier = tuple[AnyParametersParser, AnyQuerier]
ParserAndQuerierTypes = tuple[Type[AnyParametersParser], Type[AnyQuerier]]

AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_AND_QUERIER_MAPPING: \
    dict[
        AggregationIntervalSeconds,
        ParserAndQuerierTypes
    ] = \
    {
        AggregationIntervalSeconds.ONE_HOUR:  (
            OneHourAggregationIntervalPostQueryParametersParser,
            OneHourQuerier
        ),
        AggregationIntervalSeconds.ONE_DAY:   (
            OneDayAggregationIntervalPostQueryParametersParser,
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

from typing import Type

from energy.logic.aggregated_consumption. \
    aggregation_interval_to_parameters_parser_and_querier_mapping import \
    (
    AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_AND_QUERIER_MAPPING,
    ParserAndQuerierTypes,
)
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters,
    EnergyConsumptionQueryRawParameters,
)
from energy.logic.aggregated_consumption.parameters_parsers import AnyParametersParser
from energy.logic.aggregated_consumption.queriers import AggregatedConsumptionQueryRows
from energy.logic.aggregated_consumption.simple import parse_aggregation_interval
from institutions.models import Facility
from users.logic import check_role_belongs_to_user, check_role_has_access_for_facility
from users.models import User, UserRole
from utils.common import get_object_by_hashed_id_or_404


class AggregatedEnergyConsumptionController:
    __PARAMETERS_PASSED_MANUALLY = ('role', 'facility', 'aggregation_interval_seconds')

    def __init__(self, user: User, parameters: EnergyConsumptionQueryRawParameters):
        self.__query_parameters = parameters
        role = get_object_by_hashed_id_or_404(
            UserRole,
            self.__query_parameters.get('role', None)
        )
        # noinspection PyTypeChecker
        self.__facility: Facility = get_object_by_hashed_id_or_404(
            Facility, self.__query_parameters.get('facility', None)
        )
        # noinspection PyTypeChecker
        self.__check_user_is_role_owner_and_role_has_access_to_facility(
            user,
            role
        )
        self.__aggregation_interval = parse_aggregation_interval(
            self.__query_parameters.get('aggregation_interval_seconds', None)
        )

    def get_consumption(self) -> AggregatedConsumptionQueryRows:
        parser, querier = self.__get_parser_and_querier()
        params = self.__compose_params_for_querier(parser)
        return querier(params).get_consumption()

    def __check_user_is_role_owner_and_role_has_access_to_facility(
            self, user: User, role: UserRole):
        # noinspection PyTypeChecker
        check_role_belongs_to_user(user, role)
        # noinspection PyTypeChecker
        check_role_has_access_for_facility(role, self.__facility)

    def __compose_params_for_querier(
            self, parser: Type[AnyParametersParser]) -> AnyQueryParameters:
        dynamic_parameters = self.__exclude_already_parsed_parameters()
        return parser(
            facility_to_get_consumption_for_or_all_descendants_if_any=self.__facility,
            aggregation_interval=self.__aggregation_interval,
            **dynamic_parameters
        ).get_parameters()

    def __exclude_already_parsed_parameters(self) -> dict[str, str]:
        return {
            key: value for key, value in self.__query_parameters.items()
            if key not in self.__PARAMETERS_PASSED_MANUALLY
        }

    def __get_parser_and_querier(self) -> ParserAndQuerierTypes:
        return AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_AND_QUERIER_MAPPING[
            self.__aggregation_interval
        ]

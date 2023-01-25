from typing import Type

from energy.logic.aggregated_consumption.aggregated_consumption_queriers import AnyQuerier
from energy.logic.aggregated_consumption.aggregation_interval_to_parameters_parser_and_querier_mapping import \
    get_parser_and_querier_for_interval
from energy.logic.aggregated_consumption.forecast import ConsumptionForecaster
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters, EnergyConsumptionQueryRawParameters,
)
from energy.logic.aggregated_consumption.parameters_builder_from_raw import ParametersBuilder
from energy.logic.aggregated_consumption.simple import (
    parse_aggregation_interval,
)
from energy.logic.aggregated_consumption.types import (
    AggregatedConsumptionData,
    RawAggregatedConsumptionData,
)
from institutions.models import Facility
from users.logic import check_role_belongs_to_user, check_role_has_access_for_facility
from users.models import User, UserRole
from utils.common import get_object_by_hashed_id_or_404


class AggregatedEnergyConsumptionController:

    def __init__(self, user: User, parameters: EnergyConsumptionQueryRawParameters):
        _ = self.__raw_parameters = parameters
        role = get_object_by_hashed_id_or_404(
            UserRole,
            _.get('role', None)
        )
        # noinspection PyTypeChecker
        self.__facility: Facility = get_object_by_hashed_id_or_404(
            Facility, _.get('facility', None)
        )
        # noinspection PyTypeChecker
        self.__check_user_is_role_owner_and_role_has_access_to_facility(
            user,
            role
        )
        self.__aggregation_interval = parse_aggregation_interval(
            _.get('aggregation_interval_seconds', None)
        )

    def get_consumption(self) -> AggregatedConsumptionData:
        querier = self.__create_querier()
        forecaster = self.__create_forecaster(
            ConsumptionForecaster,
            querier.parameters,
            querier.get_consumption()
        )
        return querier.formatter.format(forecaster.get_consumption_forecast())

    def __get_parameters_builder(self) -> ParametersBuilder:
        return ParametersBuilder(
            self.__facility, self.__aggregation_interval, self.__raw_parameters
        )

    def __create_forecaster(
            self, forecaster_class: Type[ConsumptionForecaster],
            parameters: AnyQueryParameters,
            raw_aggregated_consumption_data: RawAggregatedConsumptionData) -> ConsumptionForecaster:
        return forecaster_class(parameters, raw_aggregated_consumption_data)

    def __create_querier(self) -> AnyQuerier:
        parser_type, querier_type = get_parser_and_querier_for_interval(self.__aggregation_interval)
        parameters = self.__get_parameters_builder().compose_parameters(parser_type)
        return querier_type(parameters)

    def __check_user_is_role_owner_and_role_has_access_to_facility(
            self, user: User, role: UserRole):
        # noinspection PyTypeChecker
        check_role_belongs_to_user(user, role)
        # noinspection PyTypeChecker
        check_role_has_access_for_facility(role, self.__facility)

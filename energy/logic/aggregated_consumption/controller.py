from energy.logic.aggregated_consumption.aggregated_consumption_queriers import \
    AggregatedConsumptionQuerier
from energy.logic.aggregated_consumption.forecast import ConsumptionForecaster
from energy.logic.aggregated_consumption.parameters_parsers import ParameterParser
from energy.logic.aggregated_consumption.simple import parse_include_forecast_parameter
from energy.logic.aggregated_consumption.types import (
    AggregatedConsumptionData, AggregatedConsumptionDataWithForecast,
)
from users.logic import check_role_belongs_to_user, check_role_has_access_for_facility
from users.models import User, UserRole
from utils.common import get_object_by_hashed_id_or_404
from utils.types import StrStrDict


class AggregatedEnergyConsumptionController:

    def __init__(self, user: User, parameters: StrStrDict):
        role = self.__extract_role(parameters)
        self.__include_forecast = parse_include_forecast_parameter(
            parameters.pop('include_forecast', None)
        )
        self.__parameters = ParameterParser(parameters).get_parameters()
        # noinspection PyTypeChecker
        self.__check_user_is_role_owner_and_role_has_access_to_facility(
            user,
            role
        )

    def get_consumption_with_optional_forecast(self) \
            -> AggregatedConsumptionData | AggregatedConsumptionDataWithForecast:
        consumption = AggregatedConsumptionQuerier(self.__parameters).get_consumption()
        if self.__include_forecast:
            consumption_with_forecast = ConsumptionForecaster(
                self.__parameters, consumption
            ).get_consumption_with_forecast()
            return consumption_with_forecast
        return consumption

    def __extract_role(self, parameters: dict[str, str]) -> UserRole:
        # noinspection PyTypeChecker
        return get_object_by_hashed_id_or_404(
            UserRole,
            parameters.pop('role_pk', None)
        )

    def __check_user_is_role_owner_and_role_has_access_to_facility(
            self, user: User, role: UserRole):
        # noinspection PyTypeChecker
        check_role_belongs_to_user(user, role)
        # noinspection PyTypeChecker
        check_role_has_access_for_facility(
            role, self.__parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        )

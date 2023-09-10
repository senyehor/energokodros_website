from energy.logic.aggregated_consumption.forecast import ConsumptionForecaster
from energy.logic.aggregated_consumption.formatters import CommonFormatter
from energy.logic.aggregated_consumption.parameters import CommonQueryParameters
from energy.logic.aggregated_consumption.parameters_parsers import ParameterParser
from energy.logic.aggregated_consumption.specific_queriers import AggregatedConsumptionQuerier
from energy.logic.aggregated_consumption.types import (
    ConsumptionWithConsumptionForecast,
    ConsumptionWithConsumptionForecastWithTotalConsumption,
    ConsumptionWithTotalConsumption, RawConsumptionRecord, RawConsumptionWithRawTotalConsumption,
)

from users.logic import check_role_belongs_to_user, check_role_has_access_for_facility
from users.models import User, UserRole
from utils.common import get_object_by_hashed_id_or_404
from utils.types import StrStrDict


class AggregatedEnergyWithOptionalForecastQuerier:

    def __init__(self, user: User, parameters: StrStrDict):
        role = self.__extract_role(parameters)
        self.__parameters = ParameterParser(parameters).get_parameters()
        # noinspection PyTypeChecker
        self.__check_user_is_role_owner_and_role_has_access_to_facility(
            user,
            role
        )

    def get_consumption_and_total_consumption_with_optional_forecast(self) -> \
            ConsumptionWithTotalConsumption \
            | ConsumptionWithConsumptionForecastWithTotalConsumption \
            | tuple[None, None]:
        querier = self.__create_consumption_querier()
        total_consumption = querier.get_total_consumption()
        if self.__parameters.include_forecast:
            raw_consumption = querier.get_raw_consumption()
            if raw_consumption:
                consumption_with_forecast = self.__make_forecast_for_actual_consumption(
                    raw_consumption,
                    querier.formatter
                )
            else:
                consumption_with_forecast = None
            return consumption_with_forecast, total_consumption
        consumption = querier.get_consumption()
        return consumption, total_consumption

    def get_all_raw_consumption_and_total_consumption_with_optional_forecast(self) -> \
            RawConsumptionWithRawTotalConsumption:
        pass

    def __make_forecast_for_actual_consumption(
            self, raw_consumption: RawConsumptionRecord,
            raw_consumption_formatter: CommonFormatter
    ) -> ConsumptionWithConsumptionForecast:
        forecaster = self.__create_forecaster(raw_consumption, raw_consumption_formatter)
        return forecaster.get_consumption_with_forecast()

    def __create_forecaster(
            self, raw_consumption: RawConsumptionRecord,
            raw_aggregation_data_formatter: CommonFormatter) -> ConsumptionForecaster:
        return ConsumptionForecaster(
            self.__parameters, raw_consumption, raw_aggregation_data_formatter
        )

    def __create_consumption_querier(self) -> AggregatedConsumptionQuerier:
        return AggregatedConsumptionQuerier(self.__parameters)

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

    def get_parameters(self) -> CommonQueryParameters:
        return self.__parameters

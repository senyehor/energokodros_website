from energy.logic.aggregated_consumption.forecast import ConsumptionForecaster
from energy.logic.aggregated_consumption.parameters import CommonQueryParameters
from energy.logic.aggregated_consumption.parameters_parsers import ParameterParser
from energy.logic.aggregated_consumption.specific_queriers import AggregatedConsumptionQuerier
from energy.logic.aggregated_consumption.types import (
    Consumption, ConsumptionRawAndFormatted, ConsumptionRawAndFormattedWithForecastRawAndFormatted,
    ConsumptionWithConsumptionForecast, TotalConsumption,
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
        self.__create_consumption_querier()

    def get_consumption_with_optional_forecast(self) -> \
            Consumption | ConsumptionWithConsumptionForecast | None:
        if self.__parameters.include_forecast:
            raw_and_formatted_consumption = self.__querier.get_raw_and_formatted_consumption()
            if raw_and_formatted_consumption:
                return self.__make_forecast_for_actual_consumption(
                    raw_and_formatted_consumption
                )
            return None
        return self.__querier.get_formatted_consumption()

    def get_raw_and_formatted_consumption_with_raw_and_formatted_optional_forecast(self) -> \
            ConsumptionRawAndFormattedWithForecastRawAndFormatted | \
            ConsumptionRawAndFormatted | None:
        raw_and_formatted_consumption = self.__querier.get_raw_and_formatted_consumption()
        if self.__parameters.include_forecast:
            if raw_and_formatted_consumption:
                return self.__make_all_raw_and_all_formatted_data_forecast_for_consumption(
                    raw_and_formatted_consumption
                )
            return None
        return raw_and_formatted_consumption

    def get_total_consumption(self) -> TotalConsumption | None:
        return self.__querier.get_formatted_total_consumption()

    def __make_forecast_for_actual_consumption(
            self, raw_consumption: ConsumptionRawAndFormatted
    ) -> ConsumptionWithConsumptionForecast:
        forecaster = ConsumptionForecaster(
            self.__parameters, raw_consumption
        )
        return forecaster.get_consumption_with_forecast()

    def __make_all_raw_and_all_formatted_data_forecast_for_consumption(
            self, raw_consumption: ConsumptionRawAndFormatted
    ) -> ConsumptionRawAndFormattedWithForecastRawAndFormatted:
        forecaster = ConsumptionForecaster(
            self.__parameters, raw_consumption
        )
        return forecaster.get_raw_and_formatted_consumption_with_raw_and_formatted_forecast()

    def __create_consumption_querier(self):
        self.__querier = AggregatedConsumptionQuerier(self.__parameters)

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

from abc import ABC, abstractmethod
from datetime import datetime

from energy.logic.run_aggregation.models_and_constants import AggregationStates


class AggregationRunnerBase(ABC):
    @abstractmethod
    def run_aggregation(self):
        ...


class AggregationStateRetrieverBase(ABC):
    @abstractmethod
    def get_state(self) -> AggregationStates:
        ...

    @abstractmethod
    def get_last_time_aggregation_was_run(self) -> datetime | None:
        ...


class AggregationStartedCheckerBase(ABC):
    @abstractmethod
    def check_aggregation_started(self) -> bool:
        ...

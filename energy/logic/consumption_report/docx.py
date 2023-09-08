import io
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from django.utils.translation import gettext as _
from docx import Document

from energy.logic.aggregated_consumption.forecast import (
    KINDERGARTEN_CONSUMPTION_PER_WEEKEND_DAY,
    KINDERGARTEN_CONSUMPTION_PER_WORKING_DAY,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import CommonQueryParameters
from energy.logic.aggregated_consumption.simple import check_institution_is_kindergarten_28
from energy.logic.aggregated_consumption.types import (
    Consumption, TotalConsumption,
)
from energy.logic.consumption_report.aggregation_interval_verbose import \
    get_aggregation_interval_verbose


class ReportCreator:
    # interval and corresponding consumption
    __CONSUMPTION_TABLE_COLUMNS_COUNT = 2
    # heading and total consumption
    __CONSUMPTION_TABLE_ADDITIONAL_ROWS_COUNT = 2

    def __init__(
            self, energy_consumption: Consumption,
            total_consumption: TotalConsumption,
            query_parameters: CommonQueryParameters
    ):
        self.__energy_consumption = energy_consumption
        self.__query_parameters = query_parameters
        self.__total_consumption = total_consumption
        self.__report = Document()

    def create_report(self) -> BytesIO:
        self.__add_current_date_and_time()
        self.__add_report_parameters_info()
        self.__add_consumption_table()
        self.__add_chart()
        self.__add_project_manager()
        return self.__export_report_to_binary()

    def __export_report_to_binary(self) -> BytesIO:
        binary_report = BytesIO()
        self.__report.save(binary_report)
        binary_report.seek(io.SEEK_SET)
        return binary_report

    def __add_current_date_and_time(self):
        date_and_time_formatted = datetime.now().strftime('%d-%m-%Y %H:%M')
        project_name = _('Система моніторингу електроспоживання - KODROS')
        self.__report.add_paragraph(f'{date_and_time_formatted} {project_name}')

    def __add_report_parameters_info(self):
        monitoring_title = self.__report.add_paragraph()
        monitoring_title.add_run(_('\nМоніторинг\n')).bold = True
        query_parameters = self.__query_parameters
        self.__report.add_paragraph(
            _(
                f'Тривалість моніторингу з {query_parameters.period_start} ' + \
                f'по {query_parameters.period_end}'
            )
        )
        monitoring_facility = self.__report.add_paragraph()
        monitoring_facility.add_run(_("Об'єкт моніторингу")).bold = True
        facility = query_parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        if facility.is_institution():
            self.__report.add_paragraph(_(str(facility)))
        else:
            self.__report.add_paragraph(_(str(facility.get_institution())))
            self.__report.add_paragraph(_(str(facility)))
        aggregation_interval_verbose = get_aggregation_interval_verbose(
            query_parameters.aggregation_interval
        )
        self.__report.add_paragraph(_(f'Інтервал агрегації: {aggregation_interval_verbose}'))

    def __add_consumption_table(self):
        table_name = self.__report.add_paragraph()
        table_name.add_run(
            _('Відомість фактичних показників споживання електроенергії')
        ).bold = True
        energy_records = self.__energy_consumption
        energy_records_count = len(energy_records)
        table = self.__report.add_table(
            cols=self.__CONSUMPTION_TABLE_COLUMNS_COUNT,
            rows=energy_records_count + self.__CONSUMPTION_TABLE_ADDITIONAL_ROWS_COUNT
        )
        table.style = 'Table Grid'
        header_row = table.rows[0]
        header_row.cells[0].text = _('Діапазон')
        header_row.cells[1].text = _('Показник електроспоживання, кВт/год')

        for record_number, consumption in enumerate(energy_records):
            table.rows[record_number + 1].cells[0].text = consumption[0]
            table.rows[record_number + 1].cells[1].text = consumption[1]

        total_row = table.rows[-1]
        total_text = total_row.cells[0].add_paragraph()
        total_text.add_run(_('Загалом')).bold = True
        total_value = total_row.cells[1].add_paragraph()
        total_value.add_run(self.__total_consumption).bold = True

    def __add_chart(self):
        interval_index, value_index = 0, 1
        # todo make get raw data where needed + redesign controller
        labels = [str(consumption_record[interval_index]) for consumption_record in
                  self.__energy_consumption]
        values = np.array(
            [float(consumption_record[value_index]) for consumption_record in
             self.__energy_consumption]
        )
        fig, ax = plt.subplots()
        ax.bar(
            labels, values, color=(1, 0.39, 0.51), hatch='//', label=_('Фактичне споживання'),
            zorder=4, alpha=0.5
        )
        is_kindergarten_28 = check_institution_is_kindergarten_28(
            self.__query_parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        )
        if self.__query_parameters.aggregation_interval == AggregationIntervalSeconds.ONE_DAY \
                and is_kindergarten_28:
            consumption_days = [
                consumption_record[interval_index] for consumption_record in
                self.__energy_consumption
            ]
            expected_consumption = np.array(
                [
                    KINDERGARTEN_CONSUMPTION_PER_WORKING_DAY if day.isoweekday() in range(1, 5)
                    else KINDERGARTEN_CONSUMPTION_PER_WEEKEND_DAY for day in consumption_days
                ]
            )
            ax.bar(
                labels, expected_consumption, color=(0.5, 1, 0), hatch=r'\\',
                label=_('Ліміт електроспоживання'), alpha=0.5, zorder=2
            )
        ax.legend()
        plt.grid(zorder=0, axis='y')
        plt.xticks(rotation=90, ha='right')
        plt.tight_layout(pad=2)
        plt.ylabel(_('кВт/год'))
        plt.title(_('Графік споживання теплової енергії'))
        image = io.BytesIO()
        plt.savefig(image, format='png', bbox_inches='tight')
        image.seek(io.SEEK_SET)
        self.__report.add_picture(image)

    def __add_project_manager(self):
        self.__report.add_paragraph(_('Науковий керівник Микола СОТНИК'))

from datetime import datetime
from io import BytesIO

from django.utils.translation import gettext as _
from docx import Document

from energy.logic.aggregated_consumption.parameters import CommonQueryParameters
from energy.logic.aggregated_consumption.types import ConsumptionWithTotalConsumption
from energy.logic.consumption_report.aggregation_interval_verbose import \
    get_aggregation_interval_verbose


class ReportCreator:
    def __init__(
            self, energy_consumption: ConsumptionWithTotalConsumption,
            query_parameters: CommonQueryParameters
    ):
        self.__energy_consumption = energy_consumption
        self.__query_parameters = query_parameters
        self.__report = Document()

    def create_report(self) -> BytesIO:
        self.__add_current_date_and_time()
        self.__add_report_meta()
        self.__add_consumption_table()
        binary_report = BytesIO()
        self.__report.save(binary_report)
        binary_report.seek(0)
        return binary_report

    def __add_current_date_and_time(self):
        date_and_time_formatted = datetime.now().strftime('%d-%m-%Y %H-%M')
        project_name = _('Система моніторингу електроспоживання - KODROS')
        self.__report.add_paragraph(f'{date_and_time_formatted} {project_name}')

    def __add_report_meta(self):
        self.__report.add_paragraph(_('Моніторинг'))
        q = self.__query_parameters
        self.__report.add_paragraph(f'Тривалість моніторингу з {q.period_start} по {q.period_end}')
        self.__report.add_paragraph(_("Об'єкт моніторингу"))
        facility_institution = \
            q.facility_to_get_consumption_for_or_all_descendants_if_any.get_root()
        self.__report.add_paragraph(_(str(facility_institution)))
        self.__report.add_paragraph(
            _(str(q.facility_to_get_consumption_for_or_all_descendants_if_any))
        )
        self.__report.add_paragraph(get_aggregation_interval_verbose(q.aggregation_interval))

    def __add_consumption_table(self):
        self.__report.add_paragraph(_('Відомість фактичних показників споживання електроенергії'))
        energy_records = self.__energy_consumption[0]
        energy_records_count = len(energy_records)
        table = self.__report.add_table(cols=2, rows=energy_records_count + 1)
        header_row = table.rows[0]
        header_row.cells[0].text = _('Діапазон')
        header_row.cells[0].text = _('Показник електроспоживання, кВт/год')

        for i, consumption in enumerate(energy_records):
            table.rows[i + 1].cells[0].text = consumption[0]
            table.rows[i + 1].cells[1].text = consumption[1]

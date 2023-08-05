
import datetime as dt
from logging import getLogger
from re import sub

from . import Reader
from ..calculate.segment import SegmentCalculator
from ..names import SEGMENT_TIME, SEGMENT_HEART_RATE
from ...diary.database import summary_column
from ...diary.model import value, text, optional_text
from ...lib.date import local_date_to_time
from ...sql.tables.segment import SegmentJournal, Segment
from ...sql.tables.statistic import StatisticJournal, StatisticName

log = getLogger(__name__)


def segments_for_activity(s, ajournal):
    return s.query(SegmentJournal). \
        filter(SegmentJournal.activity_journal == ajournal). \
        order_by(SegmentJournal.start).all()


class SegmentDiary(Reader):

    @optional_text('Segments')
    def _read_date(self, s, date):
        tomorrow = local_date_to_time(date + dt.timedelta(days=1))
        today = local_date_to_time(date)
        for sjournal in s.query(SegmentJournal).join(Segment). \
                filter(SegmentJournal.start >= today,
                       SegmentJournal.start < tomorrow). \
                order_by(SegmentJournal.start).all():
            stats = [value(sub('^Segment ', '', field.statistic_name.name), field.value,
                           units=field.statistic_name.units, measures=field.measures_as_model(date))
                     for field in (self.__field(s, date, sjournal, name)
                                   for name in (SEGMENT_TIME, SEGMENT_HEART_RATE))
                     if field]
            if stats:
                yield [text(sjournal.segment.name, tag='segment')] + stats

    @staticmethod
    def __field(s, date, sjournal, name):
        return StatisticJournal.at_date(s, date, name, SegmentCalculator, sjournal.segment, source_id=sjournal.id)

    @optional_text('Segments')
    def _read_schedule(self, s, date, schedule):
        for segment in s.query(Segment).all():
            segment_rows = [list(summary_column(s, schedule, date, name))
                            for name in self.__names(s, segment, SEGMENT_TIME, SEGMENT_HEART_RATE)]
            segment_rows = list(filter(bool, segment_rows))
            if segment_rows:
                yield [text(segment.name)] + segment_rows

    @staticmethod
    def __names(s, segment, *names):
        for name in names:
            sname = s.query(StatisticName). \
                filter(StatisticName.name == name,
                       StatisticName.constraint == segment,
                       StatisticName.owner == SegmentCalculator).one_or_none()
            if sname:
                yield sname


import datetime as dt
from tempfile import TemporaryDirectory
from tests import LogTestCase

from sqlalchemy.sql.functions import count

from ch2.commands.args import bootstrap_dir, m, V, mm, DEV
from ch2.config import default, getLogger
from ch2.sql import Source
from ch2.sql.tables.timestamp import Timestamp
from ch2.sql.utils import add

log = getLogger(__name__)


class TestTimestamp(LogTestCase):

    def test_set(self):
        with TemporaryDirectory() as f:
            args, sys, db = bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            with db.session_context() as s:
                source = add(s, Source())
                n = s.query(count(Timestamp.id)).scalar()
                self.assertEqual(n, 0)
                Timestamp.set(s, TestTimestamp, source=source)
                n = s.query(count(Timestamp.id)).scalar()
                self.assertEqual(n, 1)
                t = s.query(Timestamp).filter(Timestamp.owner == TestTimestamp).one()
                self.assertAlmostEqual(t.time.timestamp(), dt.datetime.now().timestamp(), 1)

    def test_context(self):
        with TemporaryDirectory() as f:
            args, sys, db = bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            with db.session_context() as s:
                with Timestamp(owner=TestTimestamp).on_success(s):
                    n = s.query(count(Timestamp.id)).scalar()
                    self.assertEqual(n, 0)
                n = s.query(count(Timestamp.id)).scalar()
                self.assertEqual(n, 1)

    def test_context_error(self):
        with TemporaryDirectory() as f:
            args, sys, db = bootstrap_dir(f, m(V), '5')
            bootstrap_dir(f, m(V), '5', mm(DEV), configurator=default)
            with db.session_context() as s:
                try:
                    with Timestamp(owner=TestTimestamp).on_success(s):
                        n = s.query(count(Timestamp.id)).scalar()
                        self.assertEqual(n, 0)
                        raise Exception('foo')
                except Exception as e:
                    self.assertEqual(str(e), 'foo')  # for some weird reason assertRaisesRegex was not working
                n = s.query(count(Timestamp.id)).scalar()
                self.assertEqual(n, 0)

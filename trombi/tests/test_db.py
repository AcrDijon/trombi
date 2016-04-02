import unittest
import os
import tempfile

from trombi.db import init


class TestDB(unittest.TestCase):
    def test_init(self):
        fd, name = tempfile.mkstemp()
        os.close(fd)
        sqluri = 'sqlite:////%s' % name

        try:
            # creating the database with initial content
            init(sqluri)

            # calling again init should be a no-op
            init(sqluri)
        finally:
            os.remove(name)

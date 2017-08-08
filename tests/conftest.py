import logging
import pytest


@pytest.fixture(scope='function')
def sneaky_filter():
    """Add (and later) remove a logging filter. This is used for "saving"
    all the emitted logrecords for a particular logger.  Then, the tests
    will assert that certain fields are present in the emitted logrecords."""

    logger = logging.getLogger('perflog')
    logger.setLevel(logging.INFO)

    class SneakyFilter(object):
        def __init__(self):
            self.log_records = []

        def filter(self, record):
            def skip(name):
                return name.startswith('_') or name in ('args', 'getMessage')

            d = {name: getattr(record, name) for name in dir(record) if not skip(name)}
            self.log_records.append(d)
            return True

    f = SneakyFilter()
    logger.addFilter(filter=f)

    try:
        yield f
    finally:
        logger.removeFilter(f)

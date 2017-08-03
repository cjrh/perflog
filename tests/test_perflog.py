import logging
import time
import pytest
import perflog


def test_perf_stats_worker(sneaky_filter):

    perflog.set_and_forget()

    time.sleep(1.1)  # CPU percent sampling takes 1 second.

    # The log records should all have been saved. Now we check them.
    log_records = sneaky_filter.log_records

    print(log_records)

    cpu = log_records[0]
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_system']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)

    assert type(log_records[1]['cpu_percent']) == float

    assert 'vmem_active' in log_records[2]
    assert 'vmem_available' in log_records[2]
    assert 'vmem_free' in log_records[2]
    assert 'vmem_inactive' in log_records[2]
    assert 'vmem_percent' in log_records[2]
    assert 'vmem_total' in log_records[2]
    assert 'vmem_used' in log_records[2]
    # BSD, OSX only:
    # assert 'vmem_wired' in log_records[2]

    assert 'net_bytes_recv' in log_records[4]
    assert 'net_bytes_sent' in log_records[4]
    assert 'net_dropin' in log_records[4]
    assert 'net_dropout' in log_records[4]
    assert 'net_errin' in log_records[4]
    assert 'net_errout' in log_records[4]
    assert 'net_packets_recv' in log_records[4]
    assert 'net_packets_sent' in log_records[4]

    assert type(log_records[5]['tot_connections']) == int

    # BSD, OSX only:
    # assert 'mem_pageins' in log_records[5]
    # assert 'mem_pfaults' in log_records[5]
    assert 'mem_rss' in log_records[3]
    assert 'mem_uss' in log_records[3]
    assert 'mem_vms' in log_records[3]


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


@pytest.mark.skipif(not perflog.ASYNCIO_ALLOWED, reason='asyncio unavailable')
def test_perflog_asyncio_single(sneaky_filter):
    import asyncio

    loop = asyncio.get_event_loop()

    loop.run_until_complete(perflog.single_pass_async(loop=loop))

    log_records = sneaky_filter.log_records

    cpu = log_records[0]
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_system']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)


@pytest.mark.skipif(not perflog.ASYNCIO_ALLOWED, reason='asyncio unavailable')
def test_perflog_asyncio_multi(sneaky_filter):

    import asyncio
    loop = asyncio.get_event_loop()

    async def run_some_then_die():
        loop.call_later(1.1, loop.stop)
        await perflog.multi_pass_async(loop=loop)

    try:
        loop.run_until_complete(run_some_then_die())
    except RuntimeError:
        pass

    log_records = sneaky_filter.log_records

    cpu = log_records[0]
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_system']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)
    assert type(cpu['cpu_user']) in (int, float)

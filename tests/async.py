import asyncio
import perflog


def test_perflog_asyncio_single(sneaky_filter):

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


def test_perflog_asyncio_multi(sneaky_filter):

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

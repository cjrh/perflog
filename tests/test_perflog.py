import time
import perflog
import socket
import threading


PORT  = 9007


def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', PORT))
    serversocket.listen(5)
    while 1:
        (s, address) = serversocket.accept()


def client_connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', PORT))


def test_perf_stats_worker(sneaky_filter):

    # Get at least one socket connection up
    server_thread = threading.Thread(target=listen)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(0.5)

    client_thread = threading.Thread(target=client_connect)
    client_thread.daemon = True
    client_thread.start()

    time.sleep(0.5)

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


if perflog.ASYNCIO_ALLOWED:
    from tests.async import test_perflog_asyncio_single, test_perflog_asyncio_multi

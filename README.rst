.. image:: https://travis-ci.org/cjrh/perflog.svg?branch=master
    :target: https://travis-ci.org/cjrh/perflog

.. image:: https://coveralls.io/repos/github/cjrh/perflog/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/perflog?branch=master

.. image:: https://img.shields.io/pypi/pyversions/perflog.svg
    :target: https://pypi.python.org/pypi/perflog

.. image:: https://img.shields.io/github/tag/cjrh/perflog.svg
    :target: https://img.shields.io/github/tag/cjrh/perflog.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20perflog-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20perflog-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/perflog.svg
    :target: https://img.shields.io/pypi/v/perflog.svg


perflog
=======

**Structured logging support for application performance and monitoring data**

Demo
----

.. code:: python

    """ My Application """

    import perflog

    def main():
        <All the usual application code goes here>


    if __name__ == '__main__':
        perflog.set_and_forget()
        main()


There are several parameters for the ``set_and_forget`` method that can be
used to change the default behaviour. For example, by default the performance
log messages will be written every 60 seconds.

Note: in addition to writing performance data to the log message itself,
``perflog`` also adds *extra logrecord fields*.  This means that if you're
using a log formatter that writes out all the fields in some kind of
structured format (say, logstash_formatter), you will find that the performance
data will also be recorded in those fields and can therefore be accessed in
tools like Kibana.

Acknowledgements
----------------

``perflog`` uses `psutil <https://github.com/giampaolo/psutil>`_ to
obtain all the process-related information. Thanks Giampaolo!

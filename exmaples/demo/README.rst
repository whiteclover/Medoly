Demo
+++++++


How to run
==========


.. code-block:: bash


   > python service.py -h


    optional arguments:
      -h, --help            show this help message and exit

    Service settings:
      -H SERVER.HOST, --server.host SERVER.HOST
                            The host of the http server (default 'localhost')
      -p SERVER.PORT, --server.port SERVER.PORT
                            The port of the http server (default 8888)
      -d, --debug           Open debug mode (default False)
      --secert_key SECERT_KEY
                            The secert key for secure cookies (default
                            '7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY=')
      -c FILE, --config FILE
                            config path (default './conf/app.conf')
      -v VERSION, --version VERSION
                            Show demo version 0.1
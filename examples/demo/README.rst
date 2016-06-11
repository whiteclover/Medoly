Demo
+++++++


App Structure
===============


.. code-block::

  ├─app
  │  │  boot.py # boot settings
  │  │  filters.py # http hook filter
  │  │  index.py # home menu
  │  │  __init__.py
  │  │
  │  ├─ asset # default static asset path
  │  ├─template # template path
  │  │  │  404.html
  │  │  │  index.html
  │  │  │  user_index.html
  │  │  │
  │  │  └─ui # ui module template path
  │  │          user.html
  │  │
  │  └─user # user module
  │          mapper.py
  │          model.py
  │          thing.py
  │          ui.py
  │          view.py
  │          __init__.py
  │
  └─conf
          app.conf

How to run
==========


.. code-block:: bash


   > python service.py -h

   usage: Demo [-h] [-H SERVER.HOST] [-p SERVER.PORT] [-d]
              [--secert_key SECERT_KEY] [-c FILE] [-v VERSION]
              [--choco.cache_path CHOCO.CACHE_PATH] [--choco.filesystem_checks]
              [--asset.url_prefix ASSET.URL_PREFIX] [--asset.path ASSET.PATH]

  optional arguments:
    -h, --help            show this help message and exit

  Service settings:
    -H SERVER.HOST, --server.host SERVER.HOST
                          The host of the http server (default 'localhost')
    -p SERVER.PORT, --server.port SERVER.PORT
                          The port of the http server (default 8880)
    -d, --debug           Open debug mode (default True)
    --secert_key SECERT_KEY
                          The secert key for secure cookies (default
                          '7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY=')
    -c FILE, --config FILE
                          config path (default '/etc/demo/app.conf')
    -v VERSION, --version VERSION
                          Show demo version 0.1

  choco template settings:
    --choco.cache_path CHOCO.CACHE_PATH
                          choco template module cache path: (default None)
    --choco.filesystem_checks
                          choco filesystem checks (default False)

  Asset settings:
    --asset.url_prefix ASSET.URL_PREFIX
                          Asset url path prefix: (default
                          '/Medoly/examples/demo')
    --asset.path ASSET.PATH
                          Asset files path (default
                          '/Medoly/examples/demo/app/asset')
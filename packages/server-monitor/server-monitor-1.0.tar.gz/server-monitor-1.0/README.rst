=====
Server-Monitor
=====

Server-Monitor is a Django app to set up the backend server side as a dependency 
for the Telegram Bot CyberLife Machine Monitor. This enables to set up periodic notifications
on your Telegram

Quick start
-----------

1. Add "machine_monitor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'machine_monitor',
    ]

2. Include the machine_monitor URLconf in your project urls.py like this::

    path('machine_monitor/', include('machine_monitor.urls')),


3. Start the development server and start the Bot

4. Use the Ip Address of your Machine to access this server

5. Use /check_status to know the status of your server

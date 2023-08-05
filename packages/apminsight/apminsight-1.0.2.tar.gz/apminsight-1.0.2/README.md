Python Application Performance Monitoring
=========================================

Monitor and optimize your Python application performance with a Site24x7 APM Insight Python agent. The agent provides you information on your application's response time, throughput, database operations, and errors. Track these metrics over time to identify where to optimize them for enhanced performance.

Before you can use an APM Insight agent to monitor metrics, ensure that you have a Site24x7 account.

Requirements : Python version 3.5.0 and above

Supported frameworks : Django, Flask

Supported components : pymysql, psycopg2, pymemcache, redis, sqlite, jinja

**Installation instructions:**

* Install APM Insight Python agent in your application directory using pip command

        pip install apminsight

* For Django applications, add **apminsight.contrib.django** as the first of **INSTALLED_APPS** in django settings.py

* For Flask applications, add **import apminsight** in the first line of main file

* Add the license key in environment **S247_LICENSE_KEY**
       
        export S247_LICENSE_KEY=<license-key>

* Restart your Django or Flask application

* Perform some transactions in your application for the agent to collect data. Log into your Site24x7 account and navigate to APM Insight and click on your application to see application metrics. 
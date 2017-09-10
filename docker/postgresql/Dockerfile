FROM ubuntu:16.04

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
USER root
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release of PostgreSQL, 9.6
RUN apt-get update -y && apt-get install -y software-properties-common python-software-properties wget
RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL 9.6 and other useful stuffs
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
    apt-get install -y postgresql-9.6 postgresql-contrib-9.6 vim sudo less

# Add configuration
COPY ./postgresql/config/pg_hba.conf /etc/postgresql/9.6/main/pg_hba.conf
COPY ./postgresql/config/postgresql.conf /etc/postgresql/9.6/main/postgresql.conf
RUN chown postgres:postgres /etc/postgresql/9.6/main/pg_hba.conf
RUN chown postgres:postgres /etc/postgresql/9.6/main/postgresql.conf

# Configure `sandrina` database
COPY ./postgresql/config/db_schema /var/lib/postgresql/db_schema
COPY ./postgresql/fill_db.py /var/lib/postgresql/fill_db.py
COPY ./postgresql/data/comuni_min.json /var/lib/postgresql/comuni_min.json
COPY ./postgresql/data/salute.json /var/lib/postgresql/salute.json
COPY ./postgresql/data/startup.json /var/lib/postgresql/startup.json
COPY ./postgresql/data/lavoro.json /var/lib/postgresql/lavoro.json
RUN chown postgres:postgres -R /var/lib/postgresql/
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install psycopg2

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# start the container starting postgresql itself, and creating the db schema
CMD service postgresql start && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_global_objects.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_comuni_table.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_comuni.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_lavoro_table.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_lavoro.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_salute_table.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_salute.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_startup_table.sql && \
    sudo -iu postgres psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_startup.sql && \
    python /var/lib/postgresql/fill_db.py comuni /var/lib/postgresql/comuni_min.json && \
    python /var/lib/postgresql/fill_db.py salute /var/lib/postgresql/salute.jso  && \
    /bin/bash


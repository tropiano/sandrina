FROM ubuntu:16.04

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
USER root
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release of PostgreSQL, 9.6
RUN apt-get update -y && apt-get install -y software-properties-common python-software-properties wget
RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL 9.6
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y postgresql-9.6 postgresql-contrib-9.6 

# Add configuration
COPY ./config/pg_hba.conf /etc/postgresql/9.6/main/pg_hba.conf
COPY ./config/postgresql.conf /etc/postgresql/9.6/main/postgresql.conf
RUN chown postgres:postgres /etc/postgresql/9.6/main/pg_hba.conf
RUN chown postgres:postgres /etc/postgresql/9.6/main/postgresql.conf
RUN /etc/init.d/postgresql start

# Configure `sandrina` database
COPY ./config/db_schema /var/lib/postgresql/db_schema
RUN chown postgres:postgres -R /var/lib/postgresql/db_schema
USER postgres
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_global_objects.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_comuni_table.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_comuni.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_lavoro_table.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_lavoro.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_salute_table.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_salute.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_startup_table.sql
RUN psql -U postgres -f /var/lib/postgresql/db_schema/create_indexes_on_startup.sql

# Expose the PostgreSQL port
USER root
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/bin/bash"]

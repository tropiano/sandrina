FROM ubuntu:16.04

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release of PostgreSQL, 9.6
RUN apt-get update -y && apt-get install -y software-properties-common python-software-properties wget
RUN add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Install PostgreSQL 9.6 client
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y postgresql-client-9.6

# Configure connections
COPY ./config/pgpass /root/.pgpass
RUN chmod 0600 /root/.pgpass
RUN chown root:root /root/.pgpass

# Set the default command to run when starting the container
CMD ["/bin/bash"] 

FROM debian:wheezy
MAINTAINER Evgeny "Akshaal" Chukreev <Evgeny.Chukreev@gmail.com>

# TIP: Add new stuff to the end of the file
# TIP: Stuff that tends to change add closer to the end of this file
# TIP: Stable stuff should be closer to the beginning...
# TIP: Remove stuff no longer needed, this will make docker image smaller. do it IN THE SAME STEP where it was installed!
# TIP: If some long step fails, it can be useful to break it into substeps in order to debug the problem

# Avoid questions from apt-get
ENV DEBIAN_FRONTEND noninteractive

# TODO!!!!!!: REMOVE
ENV http_proxy="http://192.168.2.93:3128"

# Install very basic stuff that we need for sure during RUNTIME operation
RUN apt-get -y update \
    && apt-get -y install --no-install-recommends \
                           python mysql-server procps nginx-full icecast2 libavcodec53 libavformat53 \
                           libsamplerate0 libmp3lame0 libshout3 ca-certificates libreplaygain1 \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

# Install pip and related things. pip wants stuff to build libs, we will install and remove those
RUN apt-get -y update \
    && TEMP_PKGS="python-pip python-dev libmysqlclient-dev git gcc g++" \
    && apt-get -y install --no-install-recommends $TEMP_PKGS \
    && pip install -e git+https://git.gitorious.org/demovibes/django-tagging-fork.git#egg=django_tagging_fork \
    && pip install Django==1.3 \
    && pip install Jinja2==2.5.5 \
    && pip install MySQL-python==1.2.3 \
    && pip install PIL==1.1.7 \
    && pip install South==0.7.3 \
    && pip install Whoosh==2.3 \
    && pip install django-authopenid==1.0.1 \
    && pip install django-extensions==0.5 \
    && pip install django-haystack==1.2.6 \
    && pip install django-wsgiserver==0.6.9 \
    && pip install flup==1.0.3.dev-20110405 \
    && pip install greenlet==0.4.2 \
    && pip install gevent==1.0.1 \
    && pip install pika==0.5.2 \
    && pip install pycountry==0.14.1 \
    && pip install python-memcached==1.47 \
    && pip install python-openid==2.2.5 \
    && pip install uwsgi==2.0.6 \
    && apt-get -y --auto-remove remove $TEMP_PKGS \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*


# TODO!!!!!: Remove "git checkout feature/docker"
# Check out demovibes from git, this is a separated step because it will change more often than the previous steps
RUN apt-get -y update \
    && service mysql start \
    \
    && TEMP_PKGS="git libreplaygain-dev libsamplerate-dev libmp3lame-dev libshout3-dev libavcodec-dev libavformat-dev gcc build-essential" \
    && apt-get -y install --no-install-recommends $TEMP_PKGS \
    \
    && cd /opt \
    && git clone https://github.com/akshaal/demovibes \
    && cd demovibes \
    && git checkout feature/docker \
    \
    && cd demosauce \
    && yes 'n' | ./configure \
    && make \
    && cd .. \
    \
    && DBPASS=$(head -c 10 /dev/urandom | base64 -w 0) \
    && SECRET=$(head -c 10 /dev/urandom | base64 -w 0) \
    && UWSGIS=$(head -c 10 /dev/urandom | base64 -w 0) \
    \
    && echo "CREATE DATABASE demovibes; GRANT ALL ON demovibes.* TO demovibes@localhost IDENTIFIED BY '$DBPASS';" | mysql -u root \
    && sed -e "s%__PATH__%/opt/demovibes%g" \
           -e "s!__DBPASS__!$DBPASS!g" \
           -e "s!__UWSGI_ID_SECRET__!$UWSGIS!g" \
           -e "s!__RANDOM_SECRET_KEY__!$SECRET!g" \
           contrib/settings_local.example.py > demovibes/settings_local.py \
    \
    && cd demovibes \
    && python manage.py syncdb \
    && python manage.py migrate \
    \
    && apt-get -y clean \
    && apt-get -y --auto-remove remove $TEMP_PKGS \
    && rm -rf /var/lib/apt/lists/* \
    \
    && service mysql stop

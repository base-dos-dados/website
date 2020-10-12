# syntax=docker/dockerfile:1.1.7-experimental

############## EXTENSIONS ###############
FROM alpine as extensions
WORKDIR /extensions
RUN apk add git
RUN git clone https://github.com/ckan/ckanext-pages.git
RUN git clone https://github.com/ckan/ckanext-repo.git
RUN git clone https://github.com/ckan/ckanext-scheming.git
RUN git clone https://github.com/NaturalHistoryMuseum/ckanext-contact.git
RUN git clone https://github.com/ckan/ckanext-googleanalytics.git
RUN git clone https://github.com/stadt-karlsruhe/ckanext-discovery.git

COPY extensions/BD_dataset.yaml /app/extensions/ckanext-scheming/ckanext/scheming/BD_dataset.yaml

################ BUILDER #################
FROM python:3.8 as builder
LABEL maintainer="Base dos Dados"
ENV PYTHONDONTWRITEBYTECODE=1 PIP_NO_PYTHON_VERSION_WARNING=1

RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/lib/apt,id=apt_list \
    --mount=type=cache,target=/var/cache/apt,id=apt_arch \
    apt-get -q -y update \
    && apt-get -y install \
        libpq-dev libxml2-dev libxslt-dev libgeos-dev libssl-dev  \
        libffi-dev postgresql-client build-essential git-core vim wget crudini

RUN python3 -m venv /venv
ENV PYTHONDONTWRITEBYTECODE=1 VIRTUAL_ENV=/venv PATH=/venv/bin:$PATH

# Setup CKAN
COPY vendor/ckan/ /ckan/
RUN --mount=type=cache,target=/root/.cache/pip/,id=pip \
    pip install -U pip setuptools==45 && \
    pip install /ckan/[requirements] && \
    pip install sqlalchemy==1.3.19 tzlocal==2.1 # Upgrade some CKAN dependencies that are emmiting warnings for py3.8

RUN cp -v /ckan/contrib/docker/ckan-entrypoint.sh /ckan-entrypoint.sh && chmod +x /ckan-entrypoint.sh

###################
## OUR ADDITIONS ##
###################

RUN --mount=type=cache,target=/root/.cache/pip/,id=pip \
    pip install ipdb flask_debugtoolbar gunicorn

# INSTALL EXTENSIONS

# COPY utils/install_extension /app/extensions/install_extension
COPY --from=extensions /extensions /app/extensions
RUN --mount=type=cache,target=/root/.cache/pip/,id=pip \
    cat /app/extensions/*/requirements.txt | egrep -v '^ *[.#]( |$)' | tee /tmp/reqs \
    && pip install -r /tmp/reqs \
    && pip install ckantoolkit ckanapi \
        python-Levenshtein unidecode nltk==3.4.5 ckanext-tagmanager # && /venv/bin/python -m nltk.downloader all
# RUN git clone https://github.com/cphsolutionslab/ckanext-customuserprivileges && cd ckanext-customuserprivileges && pip install -e .


##### INSTALL Basedosdados Files

WORKDIR /app

# COPY configs
COPY ./utils/run_development /app/
COPY ./configs/ /app/configs/
RUN crudini --merge --inplace ./configs/ckan.ini < ./configs/ckan.prod.ini && \
    crudini --set --inplace ./configs/ckan.ini server:main ckan.plugins "$(crudini --get ./configs/ckan.ini server:main ckan.plugins) $(crudini --get ./configs/ckan.ini server:main ckan.plugins_prod)"
COPY ./wsgi.py /app/wsgi.py

######### FINAL IMAGE ###########
FROM python:3.8-slim
WORKDIR /app
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
        CMD curl -f http://localhost:5000 || exit 1
ENTRYPOINT ["/ckan-entrypoint.sh"]

ENV CKAN_STORAGE_PATH=/app/uploads CKAN_INI=/app/configs/ckan.ini
ENV PIP_NO_PYTHON_VERSION_WARNING=1 PYTHONDONTWRITEBYTECODE=1
ENV VIRTUAL_ENV=/venv PATH=/venv/bin:$PATH

# System dependencies
RUN --mount=type=cache,target=/var/lib/apt,id=apt_list --mount=type=cache,target=/var/cache/apt,id=apt_arch \
        apt-get update && apt-get install -y curl htop vim

# Get files 

COPY --from=extensions /extensions /app/extensions
COPY --from=builder /venv /venv
COPY --from=builder /ckan-entrypoint.sh /ckan-entrypoint.sh

# Install extensions
RUN --mount=type=cache,target=/root/.cache/pip/,id=pip \
    pip install `for i in /app/extensions/*; do echo -e $i; done`
COPY ckanext-basedosdados /app/ckanext-basedosdados
RUN --mount=type=cache,target=/root/.cache/pip/,id=pip \
    pip install -e /app/ckanext-basedosdados
COPY --from=builder /app/run_development /app/configs/ /app/wsgi.py /app/
RUN --mount=type=cache,target=/var/lib/apt,id=apt_list --mount=type=cache,target=/var/cache/apt,id=apt_arch \
        apt-get install -y postgresql-client
        # libpq-dev libxml2-dev libxslt-dev libgeos-dev libssl-dev  \
        # libffi-dev postgresql-client build-essential git-core vim wget crudini
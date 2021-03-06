FROM continuumio/miniconda3

RUN apt-get -qq update --yes \
 && apt-get -qq install --yes --no-install-recommends \
    build-essential git make postgresql-client \
    ca-certificates wget locales \
 && rm -rf /var/lib/apt/lists/*

#Set locale
RUN sed -i -e "s/# pt_BR.*/pt_BR.UTF-8 UTF-8/" /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=pt_BR.UTF-8

# Configure conda-channels
RUN conda config --add channels conda-forge \
  && conda update --all --yes --quiet \
  && conda clean -afy

# Copy environment file to tmp/
ARG PYTHON_VERSION
COPY environment-${PYTHON_VERSION}.yml /tmp/environment.yml

# Use environment to update the env base
RUN conda env update --file /tmp/environment.yml --name base \
  && conda clean -afy

# Create deploy user
ARG HOST_UID
ARG HOST_GID
COPY docker/prepare_permission.sh /prepare_permission.sh
RUN /prepare_permission.sh
# copy code to the container and attribute permissions to user
RUN mkdir /srv/deploy/logs \
  && chown -R deploy:deploy /srv/deploy/logs
# folders
COPY --chown=deploy:deploy docker  /srv/deploy/docker
COPY --chown=deploy:deploy AlertaDengue  /srv/deploy/AlertaDengue
# files
COPY --chown=deploy:deploy requirements.txt example_env_file /srv/deploy/

# Create script activate environment
RUN echo 'source /opt/conda/bin/activate base && exec "$@"' > activate.sh
RUN chmod +x /activate.sh
WORKDIR /srv/deploy/AlertaDengue

RUN cp -p /srv/deploy/example_env_file /srv/deploy/.env_staging

EXPOSE 8000
USER deploy

ENTRYPOINT ["bash", "/activate.sh"]
CMD ["/srv/deploy/AlertaDengue/runwsgi.sh"]

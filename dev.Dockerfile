# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Install Tensorflow
RUN pip install --quiet --no-cache-dir \
    'tensorflow==2.2.0' && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

RUN pip install --quiet --no-cache-dir pystan

RUN pip install --quiet --no-cache-dir fbprophet

RUN pip install --quiet --no-cache-dir plotly

RUN pip install --quiet --no-cache-dir dash

RUN pip install --quiet --no-cache-dir dash-bootstrap-components

RUN pip install --quiet --no-cache-dir chart_studio

RUN jupyter labextension install jupyterlab-plotly@4.10.0

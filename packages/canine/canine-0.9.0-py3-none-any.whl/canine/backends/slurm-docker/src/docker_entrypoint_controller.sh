#!/bin/bash

. /gcsdk/google-cloud-sdk/path.bash.inc

sudo mysqld &
/usr/local/share/slurm_gcp_docker/src/provision_server.py
export SLURM_CONF=/mnt/nfs/clust_conf/slurm/slurm.conf
/bin/bash

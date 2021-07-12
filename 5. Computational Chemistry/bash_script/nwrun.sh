#!/bin/bash
JOB=$1
export SLURM_NTASKS_PER_NODE=14
ompi nwchem $JOB.nw >& $JOB.nw.output


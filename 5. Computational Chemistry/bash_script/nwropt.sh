#!/bin/bash
# Скрипт подготавливает к расчёту .nw и .pdb файлы
# Первый параметр - название инпута, второй - счётчик цикла i
# 
JOB=$1
i=$2
export SLURM_NTASKS_PER_NODE=14
cp $JOB.nw $JOB-$i.nw
sed -i "1s/a2r/a2r-${i}/" ./$JOB-$i.nw
sed -i "2s/a2r/a2r-${i}/" ./$JOB-$i.nw
sed -i "11s/a2r/a2r-${i}/" ./$JOB-$i.nw
sed -i "12s/a2-st.pdb/a2-st-${i}.pdb/" ./$JOB-$i.nw
sed -i "88s/a2r/a2r-${i}/" ./$JOB-$i.nw
sed -i "89s/a2r/a2r-${i}/" ./$JOB-$i.nw
sed -i "97s/a2r/a2r-${i}/" ./$JOB-$i.nw
sed -i "137s/a2r/a2r-${i}/" ./$JOB-$i.nw
ompi nwchem $JOB-$i.nw >& $JOB-$i.nw.output
#sleep 20m

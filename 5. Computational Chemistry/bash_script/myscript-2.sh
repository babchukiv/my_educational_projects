#!/bin/bash

JOB=$1

echo
echo "Begining to calculate "
echo

i=1
while [ $i -lt 100 ]  # test ! -f ./a2-F.pdb
	do
	
	echo
	echo Start for $i\-th calculation
	echo
	
	cp a2-st.pdb $JOB-st-$i.pdb # создание текущего пдб, который будем изменять
	cp $JOB.nw $JOB-$i.nw
		sed -i "1s/a2r/a2r-${i}/" ./$JOB-$i.nw
		sed -i "2s/a2r/a2r-${i}/" ./$JOB-$i.nw
		sed -i "11s/a2r/a2r-${i}/" ./$JOB-$i.nw
		sed -i "12s/a2-st.pdb/a2-st-${i}.pdb/" ./$JOB-$i.nw
		sed -i "88s/a2r/a2r-${i}/" ./$JOB-$i.nw
		sed -i "89s/a2r/a2r-${i}/" ./$JOB-$i.nw
		sed -i "97s/a2r/a2r-${i}/" ./$JOB-$i.nw
		sed -i "137s/a2r/a2r-${i}/" ./$JOB-$i.nw
	sbatch -N 8 -p test nwropt.sh $JOB $i & # получение первого rst
#	PID1=$!        # maybe sleep here!!!!
#	wait $PID1     # maybe sleep here!!!!
	
	echo
	echo Waiting for 15 minuets
	echo
	sleep 15m # Поправить на 20m
	
	if test -f a2r-$i\.rst
	then
	
		echo
		echo Begining to write new pdb-file after $i\-th calculation 
		echo
		
		cp rtp.nw rtp-$i.nw # создание текущего скрипта по переделыванию rst в pdb
		sed -i "1s/RCNI/${JOB}r-${i}/" ./rtp-$i.nw
		sed -i "3s/INCR.rst/${JOB}r-${i}.rst/" ./rtp-$i.nw
		sed -i "4s/INCR.pdb/${JOB}r-${i}-l.pdb/" ./rtp-$i.nw
		
		sbatch -N 2 -p test nwrun.sh rtp-$i & # получение pdb из rst
		echo
		echo Waiting for 5 minuets
		echo
		echo New .rst was created
		sleep 5m
#	 	PID2=$!      		# maybe sleep here!!!
#	  	wait $PID2   		# maybe sleep here!!!
		
		if test -f $JOB\r-$i-l.pdb
		then
			echo End of the $i\-th calculation
			echo
			cp $JOB\r-$i-l.pdb a2r-$i-tmp.pdb # сохранение текущего pdb
			cp $JOB\r-$i-l.pdb a2-st.pdb # переименование для повтороного запуска цикла
			
		else
			echo
			echo "Error with creation of new .pdb file"
			echo
		fi
	else
		echo
		echo "Error with first calculation: there is no .rst file"
		echo
	fi
	if test -f ./a2-F.pdb
	then
		echo
		echo -F.pdb file was created after $i\-th calculation
		break
	else
		echo
		echo Calculation $i was done without creating -F.pdb file
		echo The work will be continued
	fi
	i=$[ $i + 1 ]
done
	

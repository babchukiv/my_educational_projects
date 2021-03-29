 package require solvate
 topology top_all36_prot.rtf 
 topology top_all36_cgenff_INHisp.rtf  
 topology toppar_water_ions.str  
 topology stl.toppar.txt  
 solvate 5btr_A_pliw.psf 5btr_A_pliw.pdb -t 15 -o 5btr_A_pliw_wb
 set everyone [atomselect top all] 	 
 measure minmax $everyone
 exit
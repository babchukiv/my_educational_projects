 package require autoionize
 topology top_all36_prot.rtf 
 topology top_all36_cgenff_INHisp.rtf  
 topology toppar_water_ions.str  
 topology stl.toppar.txt
 autoionize -psf 5btr_A_pliw_wb.psf -pdb 5btr_A_pliw_wb.pdb -neutralize -o 5btr_A_pliw_wb_i
 exit
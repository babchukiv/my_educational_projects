if {[info exist qm]} {
    set y ""
    set c {}
    foreach a [lsort [$qm get {element serial}]] {
            set x [lindex $a 0]
            if { ($x!=$y) && ($y!="")} {
                puts "&QM_KIND $y"
                puts "	MM_INDEX [lsort -integer $c]"
                puts "&END"
                set c {}
            }
            lappend c [lindex $a 1]
            set y $x
    }
    puts "&QM_KIND $y"
    puts "	MM_INDEX [lsort -integer $c]"
    puts "&END"
    puts ""
    set qm_caps [lsort -unique -integer [join [$qm getbonds]]]
    set qmid [$qm get index]
    set diff {}
      foreach i $qm_caps {
        if {[lsearch -exact $qmid $i]==-1} {
          lappend diff $i
        }
      }
    set caps [atomselect top "index $diff"]
    set caps_qm  [lsort -unique -integer [join [$caps getbonds]]]
    set caps_b [$caps getbonds]
    set diff {}
      foreach i $caps_b {
      	foreach j $i {
       	 if {[lsearch -exact $qmid $j]!=-1} {
         lappend diff $j
       	 }
	}
      }
#puts "Caps:"
#puts "[$caps get serial]"
set caps2 {}
foreach i $diff {lappend caps2 [expr $i+1]}
#puts $caps2
    set i 0
    foreach cap [$caps get serial] {
    	puts "# [lindex [$caps get {resname resid}] $i]" 
    	puts "&LINK"
    	puts "	MM_INDEX $cap"
    	puts "	QM_INDEX [lindex $caps2 $i]"
    	puts "	QM_KIND H"
#    	puts "	ALPHA_IMOMM 1.41"
    	puts "&END LINK"
    	puts ""

    	incr i 1
    } 
} else {
    puts "QM atom selection should be in the \$qm variable!"
}

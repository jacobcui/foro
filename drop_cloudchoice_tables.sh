#!/bin/bash
tables="cloudchoice_cloudmodel     
 cloudchoice_component      
 cloudchoice_componentname  
 cloudchoice_os             
 cloudchoice_plan           
 cloudchoice_product        
 cloudchoice_service        
 cloudchoice_unit           
 cloudchoice_vendor       
"
for table in $tables; do
    mysql -ujacob -pnoddy4U mysite -e "drop table $table"
done

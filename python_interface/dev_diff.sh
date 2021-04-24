#!/bin/bash

dev_diff(){
  ls /dev | sed -r $'s/ /\\n/g' > /tmp/diff_1 ;
  bool_dev_diff=false ;
  echo "Please plug or unplug device now..." ;
  while [[ $bool_dev_diff == false ]]; do 
    ls /dev | sed -r $'s/ /\\n/g' > /tmp/diff_2;
    if [[ $(diff /tmp/diff_1 /tmp/diff_2) ]]; then
      echo -E "device diff detected, waiting a few seconds for other drivers to start..." ;
      echo
      sleep 3 ;
      ls /dev | sed -r $'s/ /\\n/g' > /tmp/diff_2;
      bool_dev_diff=true;
      break;
    fi;
  done ;
diff /tmp/diff_1 /tmp/diff_2 ; }

dev_diff



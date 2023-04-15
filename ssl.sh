#!/bin/bash

help_function()
{
   echo ""
   echo "Usage: $0 -d directory -s source -c count -w weights"
   echo -e "\t-d Provide path to where the dataset should be saved"
   echo -e "\t-s Provide path to video"
   echo -e "\t-c Provide integer from where count should start"
   echo -e "\t-w Provide path to weights (.pt) file"
   exit 1 # Exit script after printing help
}

while getopts "d:s:c:w:" opt
do
   case "$opt" in
      d ) directory="$OPTARG" ;;
      s ) source="$OPTARG" ;;
      c ) count="$OPTARG" ;;
      w ) weights="$OPTARG" ;;
      ? ) help_function ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$directory" ] || [ -z "$source" ] || [ -z "$count" ] || [ -z "$weights" ]
then
   echo "Some or all of the parameters are empty";
   help_function
fi

name=$directory"-ssl"
python ../yolov5-custom-components/dataset-creation.py -d $directory -s $source -c $count
python ../yolov5/detect.py --source $directory --weights $weights --device 0 --name $name --save-txt
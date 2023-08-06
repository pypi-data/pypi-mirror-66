# Python Find imported Module
pip3 install findimport

# Example:
# findownimportfile
if the source file in /mnt/c/workspace/example/source_code.py

## Input:
python3 -m findimport  --source source_code.py --path /mnt/c/workspace/ or /mnt/c/workspace/example

## Output:
/mnt/c/workspace/example/own_import_find.txt

## Input:
python3 -m findimport  --source source_code.py --path /mnt/c/workspace/ or /mnt/c/workspace/example --save_text /mnt/c/workspace/imported_file.txt
## Ouput:
/mnt/c/workspace/imported_file.txt



$ python3.7
>> import findimport
>> import_list = findimport.find_own_import(source,path)
>> print(import_list)
 ['/mnt/c/workspace/example/other_code.py',...]

# findownimportfile
python3 -m findimport  --source source_code.py --path 'dummystring' --find_all_import


S$ python3.7
>> import findimport
>> import_list = findimport.find_all_import(source)






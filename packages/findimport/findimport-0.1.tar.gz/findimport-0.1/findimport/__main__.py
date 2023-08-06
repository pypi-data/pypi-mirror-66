import subprocess
import argparse
import os
#
   
def find_own_import(source,path):
   data = subprocess.getoutput('python3.7 -v '+source)
   data = data.split('\n')
   own_import = []
   for i in data:
      if '# '+path in i:
         own_import.append(i.split('matches')[-1])
   
   return own_import

def find_all_import(source):
   data = subprocess.getoutput('python3.7 -v '+source)
   data = data.split('\n')
   all_import = []
   for i in data:
      if 'import' in i:
         all_import.append(i)
   
   return all_import
   
def main(args):
   args.save_text = args.save_text.replace('.py','.txt')
   if not (args.find_all_import):
      data = find_own_import(args.source,args.path)
      # print(args.save_text)
      with open(args.save_text,'w') as f:
         f.write('\n'.join(data))
      print(data)
      print('Text file saved in location',args.save_text)
   else:
      data = find_all_import(args.source)
      with open(args.save_text,'w') as f:
         f.write('\n'.join(data))
      print(data)
      print('Text file saved in location',args.save_text)
       

if __name__ == '__main__':
      #Create the parser
   my_parser = argparse.ArgumentParser(description='get the source code file path')

   # Add the arguments
   my_parser.add_argument('--path',
                        type=str,
                        required=True,
                        help='Source code path only not with source code name \n example: /path/path2/ not /path/path2/source_code.py')
   my_parser.add_argument('--source',
            type=str,
            required=True,
            help='Source code file name \n example: source_code.py')
   my_parser.add_argument('--save_text',
            type=str,
            default='',
            help='path')
   my_parser.add_argument('--find_all_import',
            action='store_true',
            help='path')
   args = my_parser.parse_args()
   print(args.path+'..............'+args.source)
   if not (args.save_text):
      if args.find_all_import:
         args.save_text = os.getcwd()+'/all_import_'+args.source
      else:
         args.save_text = os.getcwd()+'/own_import_'+args.source
   main(args)
      

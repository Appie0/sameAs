
import gzip
import glob
from urllib.parse import urlparse
import collections


# The location of the data
ZIPFILES = '/LOD-Laundromat/**/**/data.nq.gz'
filelist = glob.glob(ZIPFILES)

file_path=""

with open("quads.nq", 'w') as output:
    for gzfile in filelist:
        try:
        

 
            file_path = gzfile
            
            # print the files' name
            print("#Starting " + file_path)
            
            #The name of the dataset's folder
            folder = gzfile.split("/",9)
                        
            with gzip.open( gzfile, 'rt',encoding='utf-8') as f:
                
                current_file = list(f)
                
                #initiate the counter
                c = collections.Counter()

                # check the first 500 lines in the file
                # and get the most frequent site

                for i in current_file[:500]:
                    src_url = i.split(">",1)[0]
                    
                    # skip "<"
                    src_url = src_url[1:]
                    
                    #get the source
                    src_site = urlparse(src_url).netloc
                    
                    #update the counter
                    c.update({src_site: 1})
    
                for line in current_file:
                
                    #check if the file contains sameAs
                    if '07/owl#sameAs' in line:
                    
                        #Get the most frequenct site in the dataset
                        mst_cmn = c.most_common(1)[0][0]
                        
                        # remove .\n from the end of the line
                        line = line.replace(' .\n','')
                        
                        # Add to the line: The most frequent site + the dataset's folder's name + end to the line
                        line = line + " <http://" + mst_cmn + "> <" + folder[7]+"/"+folder[8]+"> .\n"

                        # output the result to the output file
                        output.write(str(line))

        # throw an error with mentioning the file's path and the error.
        # then store it to the exception File. 
        except Exception as err:
            with open("exception.txt", "a") as error:
                error.write(str(file_path))
                error.write(" Error in: {}".format(err))



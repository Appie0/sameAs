from hdt import HDTDocument

#import the HDT file
document = HDTDocument("/scratch/wbeek/data/sameas-meta/data.hdt")

# the intersection function
def intersection(lst1, lst2):  
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3

i=""

try:
    #write the identity statement in ids.nq
    with open("ids.nq", "w") as output:
        #get the triples from quads.nq
        with open("quads.nq", "r") as f:
            # if a triple does not have an id write it in no_match
            with open("no_match.txt", "w") as noMatch:
            
                for i in f:
                    # get the subject from the triple        
                    subject = i.split("<")[1][:-2]
                    # Get the identity statements of the subject 
                    triple1, card1 = document.search_triples("","http://www.w3.org/1999/02/22-rdf-syntax-ns#subject",subject)
                    #get the object from the triple
                    obj =  i.split("<")[3][:-2]
                    # get the identity statement of the object
                    triple2, card2 = document.search_triples("","http://www.w3.org/1999/02/22-rdf-syntax-ns#object",obj)
                    
                    # create lists
                    sub_lst, obj_lst = []

                    # Append identity statements to lists
                    
                    for a,b,c in triple1:
                        sub_lst.append(a)
                    for a,b,c in triple2:
                        obj_lst.append(a)
                        
                    # get the intersection of the lists
                    c = intersection(sub_lst,obj_lst)
                    
        
                    # if no match write it in noMatch otherwise in output.
                    if str(c) == "[]":
                        noMatch.write(i)
                    else:
                        output.write(str(c)+"\n")
                        
# write the error and the triple in case of an exception
except Exception as err:
    with open("exception.txt", "a") as error:
        error.write(i + "\n"+ str(err))

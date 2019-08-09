import asyncio
import os
import urllib.request
from objbrowser import browse

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))
        
def get_class_members(klass):
    ret = dir(klass)
    if hasattr(klass,'__bases__'):
        for base in klass.__bases__:
            ret = ret + get_class_members(base)
    return ret


def uniq( seq ): 
    """ the 'set()' way ( use dict when there's no set ) """
    return list(set(seq))


def get_object_attrs( obj ):
    # code borrowed from the rlcompleter module ( see the code for Completer::attr_matches() )
    ret = dir( obj )
    ## if "__builtins__" in ret:
    ##    ret.remove("__builtins__")

    if hasattr( obj, '__class__'):
        ret.append('__class__')
        ret.extend( get_class_members(obj.__class__) )

        ret = uniq( ret )

    return ret
     


       
        
async def download_coroutine(url):
    #"A coroutine to download the specified url"
    request = urllib.request.urlopen(url)
    filename = os.path.basename(url)
    
    with open(filename, 'wb') as file_handle:
        while True:
            chunk = request.read(1024)
            if not chunk:
                break
            file_handle.write(chunk)
    msg = 'Finished downloading {filename}'.format(filename=filename)
    return msg
 
async def main(urls):
    """
    Creates a group of coroutines and waits for them to finish
    """
    coroutines = [download_coroutine(url) for url in urls]
    
    completed, pending = await asyncio.wait(coroutines)
    #for item in completed:
        #print(vars(item))    
        #for att in dir(item):
            #print (att, getattr(item,att))        
    #for item in dir(completed):
        #print (item, getattr(completed,item))    
        
    #list(filter(lambda x:callable(getattr(completed,x)),completed.__dir__()))   
           
    #for item in completed:
        #print(item.current_task())
        #print(get_object_attrs(item) )
    
 
if __name__ == '__main__':
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
          #  "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
          #  "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
          #  "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]
 
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
        browse(locals()) 
    finally:
        event_loop.close()

 
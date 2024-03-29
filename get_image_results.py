import re
import os.path
import sys
import subprocess

def main(argv):
    (html_file,output_dir) = process_args(argv)
    f = open(html_file)
    lines = f.readlines()
    f.close()
    
    href = re.compile(r'imgurl=(?P[^&]+)&')
    
    url_list = []
    for line in lines:
        matches = href.findall(line)
        if matches is None:
            continue

        # filter out urls that are not under reviews
        url_list += filter(lambda s: s.find('reviews') > 0, matches)
    
    for url in url_list:
        filename = os.path.join(output_dir,make_filename(url))
        retcode = subprocess.call(['curl',url,'-o',filename])
        
def process_args(argv):
    argc = len(argv)
    if argc < 3:
        print "Usage: get_image_results.py  "
        sys.exit()

    args = map(lambda s: s.strip(), argv[1:])

    # Make sure file exists
    if not os.path.exists(args[0]):
        print 'File "%s" does not exist.' % args[0]
        sys.exit()

    # Make sure directory exists
    if not os.path.exists(args[0]):
        print 'Directory "%s" does not exist.' % args[1]
        sys.exit()

    return tuple(args)

def make_filename(url):
    # first remove address
    ix = url.find('reviews/') + 8
    
    # now remove samples and distortion if they exist in the name
    smaller = url[ix:].lower()
    smaller = smaller.replace('/','_')
    smaller = smaller.replace('samples_','')
    smaller = smaller.replace('distortion_','')
    return smaller

if __name__ == "__main__":
    main(sys.argv)  

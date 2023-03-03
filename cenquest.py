import argparse
import censys

def banner():
    print(("""%s
   ____                   ___                         _   
  / ___|   ___   _ __    / _ \   _   _    ___   ___  | |_ 
 | |      / _ \ | '_ \  | | | | | | | |  / _ \ / __| | __|
 | |___  |  __/ | | | | | |_| | | |_| | |  __/ \__ \ | |_ 
  \____|  \___| |_| |_|  \__\_\  \__,_|  \___| |___/  \__|
                                                      
                  %s%s# Coded By ReverseTEN - http://github.com/ReverseTEN%s
    """ % ('\033[91m', '\033[0m', '\033[93m', '\033[0m')))


def parse_args():
    parser = argparse.ArgumentParser(
        description='Search for information using Censys',
        epilog='Example usage: python my_script.py -q "80.http.get.headers.server: Apache" -p 3'
    )
    parser.add_argument('-q', '--query', help='search query', type=str , required=True)
    parser.add_argument('-p','--pages',help='number of pages to retrieve',type=int,required=True)

    args = parser.parse_args()
    return args


if __name__=='__main__':
    banner()
    args = parse_args()
    censys.query=args.query
    censys.PageNm=args.pages
    censys.run()
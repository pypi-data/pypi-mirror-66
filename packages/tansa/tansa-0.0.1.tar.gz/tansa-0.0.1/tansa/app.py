from . import finder
from . import jreader

import sys

def main():
    file_list = finder.FileFinder(sys.argv[1]).file_list
    print(jreader.JReader().json_dispenser(file_list))

if __name__ == '__main__':
    main()
    sys.exit(main())
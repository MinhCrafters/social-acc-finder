#!/usr/bin/python3

import sys


if __name__ == "__main__":
    major = sys.version_info[0]
    minor = sys.version_info[1]

    python_version = str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])

    if major != 3 or major == 3 and minor < 6:
        print("SocialAccFinder requires Python 3.6+\nYou are using Python %s, which is not supported by SocialAccFinder" % (python_version))
        sys.exit(1)

    import SocialAccFinder
    SocialAccFinder.main()

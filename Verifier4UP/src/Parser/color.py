red_none = '\033[1;31m%s\033[0m'
green_none = '\033[1;32m%s\033[0m'
yellow_none = '\033[1;33m%s\033[0m'
blue_none = '\033[1;34m%s\033[0m'
purple_none = '\033[1;35m%s\033[0m'
cyan_none = '\033[1;36m%s\033[0m'

non_black = '\033[1;40m%s\033[0m'
non_red = '\033[1;41m%s\033[0m'
non_green = '\033[1;42m%s\033[0m'
non_yellow = '\033[1;43m%s\033[0m'
non_blue = '\033[1;44m%s\033[0m'
non_purple = '\033[1;45m%s\033[0m'
non_cyan = '\033[1;46m%s\033[0m'
non_white = '\033[1;47m%s\033[0m'


blue_white = '\033[1;34;47m%s\033[0m'

if __name__ == "__main__":
    print(red_none%"This is a test.")

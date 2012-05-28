import sys, termios, fcntl

try:
    from msvcrt import getch
except ImportError:
    # From http://docs.python.org/faq/library#how-do-i-get-a-single-keypress-at-a-time
    def getch():
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] &= ~termios.ICANON #& ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

        try:
            while 1:
                try:
                    c = sys.stdin.read(1)
                    return c
                except IOError: pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

import select
import sys
import termios
import re
def kbhit():
		fd = sys.stdin.fileno()
		r = select.select([sys.stdin],[],[],0.01)
		rcode = ''
		if len(r[0]) >0:
			rcode  = sys.stdin.read(1)
		return rcode
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
new_settings = old_settings
#new_settings[3] = new_settings[3] & ~termios.ISIG
new_settings[3] = new_settings[3] & ~termios.ICANON
new_settings[3] = new_settings[3] & ~termios.ECHONL
termios.tcsetattr(fd,termios.TCSAFLUSH,new_settings)
reg = re.compile('[nNMm]')
def run():
		while True:
				c = kbhit()
				if len(c)>0:
						if c == 'q':
							return c	
						if reg.match(c):
							if c.upper() == 'N':
								return False
							else:
								return True
				

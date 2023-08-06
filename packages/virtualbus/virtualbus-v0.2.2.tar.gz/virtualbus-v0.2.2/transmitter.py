#!/usr/bin/env python3

from virtualbus.client import Client

import random
import time


def main():
	try:
		b = Client(host="127.0.0.1", port=8888, logging=False)
		while True:
			v = random.randint(0,100)
			msg = "\033[31m{}: {}\033[m".format( "Speed", str(v) )

			b.sent(msg)
			print("Sending: {}".format(msg))

			time.sleep( 0.1 )

	except KeyboardInterrupt as e:
		pass


if __name__ == "__main__":
	main()

#!/usr/bin/env python3

from virtualbus.client import Client

import random


def main():
	try:
		b = Client(host="127.0.0.1", port=8888, logging=False)
		while True:
			msg = b.receive()
			print("Received: '{}'".format(msg))

	except KeyboardInterrupt as e:
		pass

if __name__ == "__main__":
	main()

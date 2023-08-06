#!/usr/bin/env python3

import socket
import time

class VBusClient():
	def __init__(self,host,port,timeout=1):
		"""
		Initializes the virtual bus
		host:    The ip address or the domain name of the server.
		port:    The port of the server.
		timeout: The time to wait after an unsuccessfull connection.
		"""
		self.host = host
		self.port = port
		self.timeout = timeout

		self.sock = None

	def _open(self):
		"""Opens a connection"""
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.sock.connect((self.host, self.port))
		except Exception as e:
			print("Could not connect to {}:{}".format(self.host,self.port))
			self.sock = None
			time.sleep(self.timeout)

	def _close(self):
		"""Closes a connection"""
		if self.sock is not None:
			time.sleep( 0.1 )
			try:
				self.sock.shutdown(1)
				self.sock.close()
			except Exception as e:
				print("Could not close socket")

	def _sent(self, msg):
		"""
		Sents a message
		msg: The message in utf-8 string format.
		"""

		if self.sock is None:
			#print("Could not sent msg")
			return False

		rv = True
		try:
			self.sock.sendall(str.encode(msg, 'utf-8'))
		except Exception as e:
			print("Could not sent msg")
			rv = False
		finally:
			return rv

	def _receive(self):
		"""Receives a message utf-8 string format"""

		if self.sock is None:
			#print("Could not receive msg")
			return None

		data = None
		try:
			data = self.sock.recv(1024)
			data = data.decode()
		except Exception as e:
			print("Could not receive msg")
			data = None
		return data

	def sent(self, msg):
		"""
		Sents a message
		msg: The message in utf-8 string format.
		"""

		self._open()
		rv = self._sent(msg)
		self._close()
		return rv

	def receive(self):
		"""Receives a message utf-8 string format"""

		self._open()
		data = self._receive()
		self._close()
		return data

def main():
	try:
		b = VBusClient("127.0.0.1", 8888)
		while True:
			b.sent("Hello from Vbus!")

			m = b.receive()

			if m is not None:
				print(m)
	except KeyboardInterrupt:
		b._close()


if __name__ == "__main__":
	main()

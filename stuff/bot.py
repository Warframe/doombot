from config.config import config
from stuff.irc import irc

class Bot:
	def __init__(self):
		self.config = config
		self.irc = irc(config)
		
	def run(self):
		while True:
			data = self.irc.recv_messages()
			if data:
				if data['message'] == "!b0t":
					self.irc.send('PRIVMSG {0} :/me im a b0t.'.format(data['channel']))
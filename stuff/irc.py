import socket, re

class irc:
	def __init__(self, config):
		self.config = config
		self.set_socket_object()
	
	def ping(self, data):
		if data.startswith('PING'):
			self.sock.send(data.replace('PING', 'PONG'))
			return 1
	
	def set_socket_object(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock = sock
		username = self.config['username'].lower()
		password = self.config['password']
		server = self.config['server']
		port = self.config['port']
		channels = self.config['channels']
		sock.connect((server, port))
		sock.send('PASS %s\r\n' % password)
		sock.send('NICK %s\r\n' % username)
		for channel in channels:
			sock.send('JOIN #%s\r\n' % channel)
			
	def recv_messages(self, amount=2048):
		data = self.recv(amount)
		self.ping(data)
		if self.check_has_message(data):
			return self.parse_message(data.strip())
			
	def recv(self, amount=2048):
		return self.sock.recv(amount)
		
	def send(self, data):
		return self.sock.send('{0}\r\n'.format(data))
		
	def check_has_message(self, data):
		return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)
	
	def parse_message(self, data):
		return {
			'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
			'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
			'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0]
		}


import subprocess
from datetime import datetime 
import os
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


class Reply():
	def __init__(self, reply):
		self.reply = reply


class Ping():
	def __init__(self, ip_addr='', **kwargs):

		self.ip_addr = ip_addr
		self.file = None
		self.filename = ''

		# Options
		self.options = {}
		self.options['log'] = kwargs.get('log', False)
		self.options['verbose'] = kwargs.get('verbose', False)


	def ping(self, num=10, verbose=False):
		for i in range(num):
			self._ping()
			if verbose or self.options['verbose']:
				print(self.filename + "Test: ", i+1)



	def _ping(self):
		result = subprocess.check_output(['ping', self.ip_addr]).decode('utf-8').split('\n')

		if self.options['verbose']:
			for i, row in enumerate(result):
				print(i, row)

		data = {'time':[], 'reply':[], 'stats':{}}

		# Save timestamp
		data['time'].append(datetime.now().isoformat())

		# Parse replies
		reply = []
		for i in range(2, 6):
			if result[i] in 'Destination Host Unreachable.':
				reply.append(None)
			elif result[i] in 'Request timed Out.':
				reply.append(None)
			else:
				reply.append(unpack_reply(result[i]))

		data['reply'].append(reply)

		# Parse Stats
		data['stats'] = unpack_stats(result[8], result[10])

		if self.options['log']:
			self._log(data, self.options['log'])

		self.file = data

		return data

	def print_ping(self, mask=['all']):
		if self.file:
			# time = self.file['time'][-1]
			# reply = self.file['reply'][-1]

			print("IP Addr: {}".format(self.ip_addr))
			print("Time: {}".format(self.file['time'][-1]))
			print("Reply: {}".format(self.file['reply'][-1]))

			for key, value in self.file['stats'].items():
				# stats[key] = value[-1]
				if key in mask or 'all' in mask:
					print("{}: {}".format(key, value[-1]))


		else:
			print("NO PING TO PRINT")





	def _log(self, data, filename):
		file = read_json(filename)
		if file:
			file['time'].extend(data['time'])
			file['reply'].extend(data['reply'])

			for key, value in data['stats'].items():
				file['stats'][key].extend(value)

			write_json(file, filename)

		else:
			write_json(data, filename)




	def load(self, filename):
		file = read_json(filename)

		# Convert time from iso string to datetime obj
		for t in file['time']:
			t = datetime.fromisoformat(t)
		self.file = file
		return file


	def plot_avg(self, start_time='', end_time=''):
		fig, ax = plt.subplots(1, 1)


		if self.file:
			ax.plot(mdates.date2num(self.file['time']), self.file['stats']['avg'], label='Average Ping [ms]', marker='o')

			# Format x axis
			formatter = mdates.DateFormatter('%m/%d/%y %H:%M')
			ax.xaxis.set_major_formatter(formatter)
			ax.xaxis.set_major_locator(ticker.AutoLocator())
			ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

			ax.set_title('Average Ping to ' + self.ip_addr)
			ax.set_ylabel('Ping [ms]')

			ax.legend(loc='best')
			fig.autofmt_xdate()
		else:
			print("No file loaded")

		return fig, ax


	def _filter_time(self, start_time, end_time):
		if self.file:
			pass

	def plot_scatter(self):
		fig, ax = plt.subplots(1, 1)

	def show(self):
		plt.grid()
		plt.show()





def read_json(filename):
	try:
		with open(filename) as myfile:
			try:
				return json.load(myfile)
			except json.decoder.JSONDecodeError:
				return None
	except FileNotFoundError:
		return None

def write_json(data, filename, mode='w', indent=4):
	with open(filename, mode) as myfile:
		json.dump(data, myfile, indent=indent)


def unpack_reply(reply):
	reply = reply.split(' ')
	try:
		time = int(reply[4][5:-2])
	except IndexError:
		time = None

	return time

def unpack_stats(transmission, roundtrip):
	stats = {'sent':[], 'recv':[], 'lost':[], 'loss':[], 'min':[], 'max':[], 'avg':[]}
	transmission = transmission.split(' ')
	roundtrip = roundtrip.split(' ')

	stats['sent'].append(int(transmission[7][:-1]))
	stats['recv'].append(int(transmission[10][:-1]))
	stats['lost'].append(int(transmission[13]))
	stats['loss'].append(int(transmission[14][1:-1]))
	stats['min'].append(int(roundtrip[6][:-3]))
	stats['max'].append(int(roundtrip[9][:-3]))
	stats['avg'].append(int(roundtrip[12][:-3]))

	return stats

def main():
	# result = subprocess.check_output(['ping', '192.168.1.1'])
	os.system('cls')
	ping = Ping('192.168.1.1', log='ping.json', verbose=False)
	ping.ping(1000)
	data = ping.load('ping.json')
	#print(data)
	ping.plot_avg()
	ping.show()


	# with open("ping.csv", "a") as myfile:
	# 	myfile.write(result.decode('utf-8'))

if __name__ == '__main__':
	main()
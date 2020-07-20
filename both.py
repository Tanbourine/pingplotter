from pingplotter.ping import Ping
import os

def ping_repeat(ip_addr, num):
	ping = []

	for name, ip in ip_addr.items():
		ping.append(Ping(ip, log=name+'.json'))

	for i in range(num):
		print("Cycle: ", i+1)
		for p in ping:
			p.ping(1)
			p.print_ping(mask=['min', 'max', 'avg'])

	return ping


def show_plots(ping):
	for p in ping:
		p.plot_avg()

	ping[0].show()

def main():

	home = '192.168.1.1'
	goog = 'google.com'
	ip_addr = {'home':home, 'google':goog}
	num = 1

	os.system('cls')
	pings = ping_repeat(ip_addr, 10000)

	#show_plots(pings)





if __name__ == '__main__':
	main()
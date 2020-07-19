from ping import Ping
import os

def main():
	# result = subprocess.check_output(['ping', '192.168.1.1'])
	os.system('cls')
	ping = Ping('google.com', log='google.json', verbose=False)
	ping.ping(1000)
	data = ping.load('google.json')
	#print(data)
	ping.plot_avg()
	ping.show()


	# with open("ping.csv", "a") as myfile:
	# 	myfile.write(result.decode('utf-8'))

if __name__ == '__main__':
	main()
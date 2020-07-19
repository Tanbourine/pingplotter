from ping import Ping
import os

def main():
	# result = subprocess.check_output(['ping', '192.168.1.1'])
	os.system('cls')
	router = Ping('192.168.1.1', log='home.json', verbose=False)
	router.load('home.json')
	router.plot_avg()

	router = Ping('google.com', log='ping.json', verbose=False)
	router.load('google.json')
	router.plot_avg()

	router.show()

	# with open("ping.csv", "a") as myfile:
	# 	myfile.write(result.decode('utf-8'))

if __name__ == '__main__':
	main()
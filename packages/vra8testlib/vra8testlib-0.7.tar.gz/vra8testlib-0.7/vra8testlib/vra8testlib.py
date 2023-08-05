import logging
import argparse
import sys


#parser = argparse.ArgumentParser(description='Write to the pipeline log')
#parser.add_argument('--logpath', required=True, type=str, help='Path of the file to log to')
#parser.add_argument('-m', '--message', required=True, type=str, help='Message to log')
#args = parser.parse_args()



class JenkinsLogger:
	def __init__(self):
		self.logger = logging.getLogger(__file__)
		self.logger.setLevel(logging.DEBUG)
		handler = logging.StreamHandler(sys.stdout)
		handler.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

	def send(self, message):
		self.logger.info(message)

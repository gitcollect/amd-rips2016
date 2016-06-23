# traces_database.py allows to access a PostGreSQL database through either the
# PgSQL or pgdb libraries and retrieve side-channel traces from such database.
# Copyright (C) 2008 Florent Flament (florent.flament@telecom-paristech.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Function allowing conversion from C binary data
from struct import unpack
import os

def parse_binary( raw_data ):
	"""
	Takes a raw binary string containing data from our oscilloscope.
	Returns the corresponding float vector.
	"""
	ins =  4   # Size of int stored if the raw binary string
	cur =  0   # Cursor walking in the string and getting data
	cur += 12  # Skipping the global raw binary string header
	whs =  unpack("i", raw_data[cur:cur+ins])[0] # Storing size of the waveform header
	cur += whs # Skipping the waveform header
	dhs =  unpack("i", raw_data[cur:cur+ins])[0] # Storing size of the data header
	cur += dhs # Skipping the data header
	bfs =  unpack("i", raw_data[cur-ins:cur])[0] # Storing the data size
	sc  =  bfs/ins # Samples Count - How much samples compose the wave
	dat =  unpack("f"*sc, raw_data[cur:cur+bfs])
	return dat

class traces_database:
	""" Class providing database IOs """
	# Data members
	__traces_folder_name = None

	def __init__(self, traces_folder_name):
		"""
		Note: folder of traces must be in the current directory 
		"""

		# store name of folder containing the traces
		self.__traces_folder_name = traces_folder_name

	def get_trace(self):
		"""
		Does not take any argument.
		Returns the next triplet (message, cipher, trace), where:
		 - message is an ascii string containing a 64 bit clear message in hexadecimal,
		 - cipher is an ascii string containing a 64 bit ciphered message in hexadecimal,
		 - trace is a float vector containing a trace during the cipher operation.
		"""
		# List all files in the folder containing traces
		files = [file for file in os.listdir('../' + self.__traces_folder_name) if not os.path.isdir(file)]

		for file in files:
			name, info = file.split('__') # split the file name into name and info
			key, message, cryptogram = info.split('_') # split the file name into key, message, and cryptogram
			key = key[2:] # remove "k=" from the key portion of the name
			message = message[2:] # remove "m=" from the message portion of the name
			cryptogram = cryptogram[2:-4] # remove "c=" and ".bin" from the cryptogram portion of the name
			raw_data = None

			path_to_file = '../' + self.__traces_folder_name + '/' + file
			with open(path_to_file, 'rb') as file_content: # the "rb" flag is crucial (read binary)
				raw_data = file_content.read()  # read contents of the binary file

			# This creates a generator from our function so that we perform the file listing step only once.
			# Calling the get_trace() only executes one loop of the for loop every time.
			yield message, cryptogram, parse_binary(str(raw_data))

def test():
	test_database = traces_database("secmatv1_2006_04_0809")

	traces = test_database.get_trace()

	# test functionality of get_trace() generator
	for i in range(10):
		message, cryptogram, data = traces.next()
		print ("msg=%s c=%s") % (message, cryptogram)

if __name__ == "__main__":
	test()

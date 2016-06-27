# amd-rips2016
Side-Channel Leakage and Countermeasure Characterization

# Original README
+-------------------------------------------------+
| Using matlab with the attack wrapper under UNIX |
+-------------------------------------------------+

mkfifo matlab_i;
mkfifo matlab_o;

0>matlab_i;
matlab_o>1;

/comelec/softs/opt/matlab/2009b/bin/matlab -nodisplay -nosplash -r attack.m

# attack.m:
# Example of prototyping code...
>> fi = fopen( 'matlab_i', 'r' );
>> fo = fopen( 'matlab_o', 'w' );
>> fprintf( fo, 'Hello world!' );
>> fread( fi, 5 )                
>> quit


Provided implementation:
We provide a reference implementation written in python, which implements a
differential power analysis based on the partitioning algorithm published by
Paul Kocher. The application needs an internet connection in order to access
to the side-channel traces. The code can be reused by participants to submit
new algorithms, and participate to the contest.

Reference implementation performance:
The reference implementation needs 2766 power consumption traces to break the
key of the default campaign "secmatv1_2006_04_0809" after having been
stabilized for 100 iterations on the good key.

Needed CPU and memory:

The reference implementation takes 4 hours and a half (resp. about one night)
on an Intel Xeon at 3.00 GHz (resp. Intel Core2 Duo at 1.66 GHz) using only
one core to break the key.
The application will use about 500 MB for itself (depending of the traces
length). Make sure the computer used to run the application has enough memory.
If your computer begins to swap, the computation might never end.

In order to run the provided application, you need to install the following
softwares:
- The PostgreSQL client with his shared libraries (the so called libpq)
- Python
- pyPgSQL
- egenix-mx-base - Allows the use of the DateTime module

The application has been fully tested on the following configurations:
. Windows Vista with:
	- PostgreSQL 8.3
	- Python 2.4.4
	- pyPgSQL 2.5.1
	- egenix-mx-base 3.1.1
. Linux Debian with:
	- PostgreSQL 8.1 (package lipq-dev)
	- Python 2.4.4
	- pyPgSQL 2.5.1
	- egenix-mx-base 3.1.1

Windows specific configuration:
On windows, the bin directory of the PostgreSQL installation directory has
to be added to the windows path environment variable, in order to make it's
DLL accessible from python.

To launch the application just execute the main.py script:
$ python main.py


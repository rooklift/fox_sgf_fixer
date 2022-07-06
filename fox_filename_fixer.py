import datetime, os

files = [f for f in os.listdir() if os.path.isfile(f)]

for f in files:
	
	if f.count("[") == 2 and f.count("]") == 2:

		pb = f.split("[")[1].split("]")[0]
		pw = f.split("[")[2].split("]")[0]

		unixtime = f.split("]")[2].split(".")[0]
		unixtime = unixtime[0:len(unixtime) - 9]		# Reduce from nanosecond down to second

		dt = datetime.datetime.fromtimestamp(int(unixtime))

		os.rename(f, "{}-{:02}-{:02} {} vs {}.sgf".format(dt.year, dt.month, dt.day, pb, pw))

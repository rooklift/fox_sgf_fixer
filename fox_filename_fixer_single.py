import datetime, os, os.path

abspath = os.path.abspath(sys.argv[1])					# Likely unneeded, this will already be absolute
dirname = os.path.dirname(abspath)
basename = os.path.basename(abspath)
	
if basename.count("[") == 2 and basename.count("]") == 2:

	pb = basename.split("[")[1].split("]")[0]
	pw = basename.split("[")[2].split("]")[0]

	unixtime = basename.split("]")[2].split(".")[0]
	unixtime = unixtime[0:len(unixtime) - 9]			# Reduce from nanosecond down to second

	dt = datetime.datetime.fromtimestamp(int(unixtime))

	new_basename = "{}-{:02}-{:02} {} vs {}.sgf".format(dt.year, dt.month, dt.day, pb, pw)

	os.rename(abspath, os.path.join(dirname, new_basename))

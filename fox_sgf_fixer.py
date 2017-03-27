import os, re, sys
import gofish


KNOWN_PLAYERS = {
	"绝艺":			"Fine Art",
	"星宿老仙":		"Gu Li",
	"潜伏":			"Ke Jie",
	"剑过无声":		"Lian Xiao",
	"airforce9":	"Kim Jiseok",
	"Eason":		"Zhou Ruiyang",
	"INDIANA13":	"Gu Zihao",
	"jpgo01":		"Iyama Yuta",
	"leaf":			"Shi Yue",
	"maker":		"Park Junghwan",
	"Master":		"AlphaGo",
	"nparadigm":	"Shin Jinseo",
}


def deal_with_file(filename):
	try:
		os.chdir(os.path.dirname(filename))

		root = gofish.load(filename)

		root.set_value("CA", "UTF-8")

		if root.properties["KM"] == ["0"]:			# Usually bogus
			root.set_value("KM", 6.5)

		for key in ["GN", "TT", "TM", "TC", "AP"]:
			root.delete_property(key)

		if "HA" in root.properties:
			if root.properties["HA"] == ["0"]:
				root.delete_property("HA")

		try:
			black, white, = re.search(r"\[(.+)\]vs\[(.+)\]\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\.sgf", filename).group(1, 2)
			if black in KNOWN_PLAYERS:
				root.safe_commit("PB", KNOWN_PLAYERS[black])
			if white in KNOWN_PLAYERS:
				root.safe_commit("PW", KNOWN_PLAYERS[white])
		except:
			pass

		rp = root.properties

		newfilename = "{} {} vs {}.sgf".format(rp["DT"][0], rp["PB"][0], rp["PW"][0])
		if os.path.exists(newfilename):
			newfilename = "{} {} vs {} ({}).sgf".format(rp["DT"][0], rp["PB"][0], rp["PW"][0], root.dyer().replace("?", "_"))

		gofish.save(newfilename, root)

	except Exception as err:
		try:
			print(err)
		except:
			print("<unprintable exception>")


def deal_with_files(filenames):
	for filename in filenames:
		deal_with_file(filename)


def main():

	if len(sys.argv) == 1:
		print("Need argument")
		sys.exit()

	for item in sys.argv[1:]:

		item = os.path.abspath(item)

		if os.path.isdir(item):
			all_things = list(map(lambda x : os.path.join(item, x), os.listdir(item)))
			all_files = list(filter(lambda x : os.path.isfile(x), all_things))
			deal_with_files(all_files)
		else:
			deal_with_file(item)


if __name__ == "__main__":
	main()

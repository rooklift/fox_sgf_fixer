import os, re, sys
import gofish


KNOWN_PLAYERS = {
	"小香馋猫":		"Chang Hao",
	"谜团":			"Chen Yaoye",
	"绝艺":			"Fine Art",
	"星宿老仙":		"Gu Li",
	"潜伏":			"Ke Jie",
	"剑过无声":		"Lian Xiao",
	"愿我能":			"Meng Tailing",
	"聂卫平":			"Nie Weiping",
	"段誉":			"Tan Xiao",
	"天选":			"Tuo Jiaxi",
	"周俊勳":			"Zhou Junxun",

	"airforce9":	"Kim Jiseok",
	"black2012":	"Li Qinchong",
	"Eason":		"Zhou Ruiyang",
	"INDIANA13":	"Gu Zihao",
	"jingjing":		"Dang Yifei",
	"jpgo01":		"Iyama Yuta",
	"kongm":		"Huang Yusong",
	"kuangren":		"Jiang Weijie",
	"leaf":			"Shi Yue",
	"maker":		"Park Junghwan",
	"Master":		"AlphaGo",
	"nparadigm":	"Shin Jinseo",
	"piaojie":		"Kang Dongyun",
	"pyh":			"Park Yeonghun",
	"shadowpow":	"Cho Hanseung",
	"smile":		"Yang Dingxin",
	"spinmove":		"An Sungjoon",
	"wonfun":		"Weon Seongjin",
	"ykpcx":		"Fan Tingyu",
}


def deal_with_file(filename):
	try:
		os.chdir(os.path.dirname(filename))

		root = gofish.load(filename)

		root.set_value("CA", "UTF-8")

		for key in ["GN", "TT", "TM", "TC", "AP"]:
			root.delete_property(key)

		if "KM" in root.properties:
			if root.properties["KM"] == ["0"]:			# Usually bogus
				root.delete_property("KM")

		if "HA" in root.properties:
			if root.get_value("HA") == "0":
				root.delete_property("HA")

		black_for_filename = root.get_value("PB")
		white_for_filename = root.get_value("PW")

		try:
			black, white, = re.search(r"\[(.+)\]vs\[(.+)\]\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\.sgf", filename).group(1, 2)
			if black in KNOWN_PLAYERS:
				root.safe_commit("PB", "{} ({})".format(black, KNOWN_PLAYERS[black]))
				black_for_filename = KNOWN_PLAYERS[black]
			if white in KNOWN_PLAYERS:
				root.safe_commit("PW", "{} ({})".format(white, KNOWN_PLAYERS[white]))
				white_for_filename = KNOWN_PLAYERS[white]
		except:
			pass

		dt = root.properties["DT"][0]

		newfilename = "{} {} vs {}.sgf".format(dt, black_for_filename, white_for_filename)
		if os.path.exists(newfilename):
			newfilename = "{} {} vs {} ({}).sgf".format(dt, black_for_filename, white_for_filename, root.dyer().replace("?", "_"))

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

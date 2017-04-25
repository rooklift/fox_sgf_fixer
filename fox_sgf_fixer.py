import os, re, sys
import gofish


KNOWN_PLAYERS = {

	# Not 100% guaranteed accurate...
	# If both a logographic name and an ASCII name
	# are known, I sometimes have both here...

	"小香馋猫":		"Chang Hao",
	"谜团":			"Chen Yaoye",
	"绝艺":			"Fine Art",
	"星宿老仙":		"Gu Li",
	"印城之霸":		"Gu Zihao",
	"风清扬":			"Hu Yaoyu",
	"孔明":			"Huang Yusong",
	"若水云寒":		"Jiang Weijie",
	"潜伏":			"Ke Jie",
	"剑过无声":		"Lian Xiao",
	"愿我能":			"Meng Tailing",
	"聂卫平":			"Nie Weiping",
	"段誉":			"Tan Xiao",
	"诸神的荣耀":		"Tang Weixing",
	"天选":			"Tuo Jiaxi",
	"杨鼎新":			"Yang Dingxin",
	"周俊勳":			"Zhou Junxun",

	"airforce9":	"Kim Jiseok",
	"Avenger007":	"Wang Yao",
	"bibibig":		"Choi Cheolhan",
	"black2012":	"Li Qincheng",
	"doomsday":		"Mi Yuting",
	"Eason":		"Zhou Ruiyang",
	"INDIANA13":	"Gu Zihao",
	"jingjing":		"Dang Yifei",
	"jpgo01":		"Iyama Yuta",
	"kongm":		"Huang Yusong",
	"kuangren":		"Jiang Weijie",
	"leaf":			"Shi Yue",
	"maker":		"Park Junghwan",
	"Master":		"AlphaGo",
	"miracle97":	"Byun Sangil",
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

		komi_string = root.get_value("KM")

		if komi_string == "0" and root.get_value("HA") == "0":		# Fox writes HA[1] if komi is really 0.
			root.set_value("KM", "6.5")

		try:
			if float(komi_string) >= 10 and "." not in komi_string:
				new_string = komi_string[0] + "." + komi_string[1:]
				root.set_value("KM", new_string)
		except:
			pass

		if root.get_value("HA") == "0":
			root.delete_property("HA")

		# Work out what names we're using for the outfile and the PB/PW tags...

		PB, PW = root.get_value("PB"), root.get_value("PW")
		black_real_name, white_real_name = None, None
		regex_PB, regex_PW = None, None
		try:
			regex_PB, regex_PW = re.search(r"\[(.+)\]vs\[(.+)\]\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\.sgf", filename).group(1, 2)
		except:
			pass

		if regex_PB in KNOWN_PLAYERS:
			black_real_name = KNOWN_PLAYERS[regex_PB]
			root.safe_commit("PB", "{} ({})".format(regex_PB, black_real_name))
		elif PB in KNOWN_PLAYERS:
			black_real_name = KNOWN_PLAYERS[PB]
			root.safe_commit("PB", "{} ({})".format(PB, black_real_name))

		if regex_PW in KNOWN_PLAYERS:
			white_real_name = KNOWN_PLAYERS[regex_PW]
			root.safe_commit("PW", "{} ({})".format(regex_PW, white_real_name))
		elif PW in KNOWN_PLAYERS:
			white_real_name = KNOWN_PLAYERS[PW]
			root.safe_commit("PW", "{} ({})".format(PW, white_real_name))

		black_for_filename = black_real_name if black_real_name else regex_PB if regex_PB else PB if PB else "Unknown"
		white_for_filename = white_real_name if white_real_name else regex_PW if regex_PW else PW if PW else "Unknown"

		# (Done)

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

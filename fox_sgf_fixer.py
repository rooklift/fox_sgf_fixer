import os, re, sys
import gofish


known_players_raw = {		# Keys get converted to lowercase later.

    # AIs

    "fuheyuqi":     "As Expected",
    "Master":       "AlphaGo",

	"符合预期":		"As Expected",
	"金毛测试":		"BensonDarr",
	"金毛陪练":		"BensonDarr",
	"돌바람":			"DolBaram",
	"石子旋风":		"DolBaram",
	"绝艺":			"Fine Art",
	"绝艺指导A":		"Fine Art A",
	"绝艺指导B":		"Fine Art B",
	"绝艺指导C":		"Fine Art C",
	"骊龙":			"Li Long Fine Art",
	"刑天":			"Xing Tian AI",

    # Humans. Not 100% guaranteed accurate...
    # If both a logographic name and an ASCII name
    # are known, I sometimes have both here...

	"195725152":           "Cai Wenxin",
	"1992peter":           "Lin Xiuping",
	"20sa":                "Song Gyusang",
	"88888888":            "Yin Hang",
	"Avenger007":          "Wang Yao",
	"Bigticket":           "Liu Yuanbo",
	"CYZW":                "Li Xiuquan",
	"Callaway":            "Iyama Yuta",
	"CaptainTee":          "Lu Junren",
	"Chelsea":             "Yang Kaiwen",
	"DFS":                 "Zhang Xuebin",
	"Darwiner":            "Tong Yulin",
	"Dayline":             "Chen Hanqi",
	"Dderozan":            "Wu Hao",
	"DuanY":               "Tan Xiao",
	"FengHaiao":           "Fu Chong",
	"Flyinghear":          "Wang Zejin",
	"INDIANA13":           "Gu Zihao",
	"LenkaK":              "Gong Yanyu",
	"Lucifer":             "Sun Tengyu",
	"Mlstar":              "Yang Yi (s)",
	"Monody":              "Gu Lingyi",
	"NightCome":           "Jiang Weijie",
	"OnceTime":            "Zhang Ziliang",
	"Paprika1":            "Wang Xiru",
	"Qsws2009":            "He Yang",
	"SJGJ":                "Zhang Xinyue",
	"SSMMD":               "Huang Yiming",
	"Shiratsuyu":          "Zheng Zijian",
	"SkyRaker":            "Chen Qirui",
	"Snipes":              "Chen Haoxin",
	"TMC":                 "Tong Mengcheng",
	"Terminator":          "Xie Erhao",
	"XIALUOTLL":           "Ding Shixiong",
	"XIALUOTLL":           "Ding Shixiong",
	"abc17":               "Ryu Minhyung",
	"adidas12":            "Hsu Chiayuan",
	"admas":               "Hyun Yoobin",
	"agasi123":            "Lu Yiquan",
	"allin6379":           "Kim Dongwoo",
	"amateur7":            "Hong Seyeong",
	"angel0412":           "Bai Xinhui",
	"artem92":             "Kachanovskyi Artem",
	"biba2017":            "Kim Seungjun",
	"bibibig":             "Choi Cheolhan",
	"bigbangG08":          "Zhang Nianqi",
	"bigstrong":           "Choi Jeong",
	"bit":                 "Han Zhuoran",
	"black2012":           "Li Qincheng",
	"blackpink":           "Lee Jihyun (m)",
	"blue18":              "Numadate Sakiya",
	"bluechip":            "Moon Joonho",
	"boltgo":              "Zhou Keping",
	"braveheart":          "Hu Yuhan",
	"bullking":            "Niu Shite",
	"bundong":             "Lee Hyungjin",
	"ch990901":            "Choi Youngchan",
	"chaosha":             "Zhou Hexi",
	"chenyichun":          "Chen Yichun",
	"chenyuch":            "Li Jianyu",
	"chic9949":            "Moon Minjong",
	"choisasi":            "Sakai Hideyuki",
	"clover77":            "Yun Junsang",
	"cocoa15":             "Kato Chie",
	"coreaface":           "Song Jihoon",
	"cpbl":                "Lin Shuyang",
	"curacao":             "Yokotsuka Riki",
	"dander":              "Zeng Zhihao",
	"darkhorse7":          "Mutsuura Yuta",
	"darkhorse7":          "Mutsuura Yuta",
	"demon8528":           "Oomote Takuto",
	"denbo":               "Yuki Satoshi",
	"dongfangmz":          "Zhu Mingsheng",
	"doomsday":            "Mi Yuting",
	"dragon13":            "You Byungyong",
	"dream09":             "Fujisawa Rina",
	"durantula":           "Kang Changbae",
	"emperor12":           "Chen Feng",
	"evc":                 "Tanaka Nobuyuki",
	"fakercarry":          "Ye Gangting",
	"fantasy123":          "Chen Yiming",
	"feihua":              "Ji Lili",
	"flash77":             "Park Hamin",
	"flash77":             "Park Hamin",
	"fohens":              "Park Seunghwa",
	"fqishi01":            "Xie Ke",
	"gangnam":             "Han Moonduk",
	"gino0408":            "Lai Junfu",
	"goldstone":           "Kim Seonryong",
	"gopro":               "Hirose Yuichi",
	"grace孤城":             "Ding Hao",
	"green0414":           "Sakai Yuuki",
	"gsdrf":               "Hu Ranmin",
	"guaitong":            "Mok Jinseok",
	"haohao2013":          "Huang Chen",
	"harnn":               "Paek Hongseok",
	"hartbeat":            "Yun Hyunbin",
	"hcyhcr":              "Hu Yaoyu",
	"heaven":              "Qiao Ran",
	"hiro120":             "Koike Yoshihiro",
	"huzihao":             "Hu Zihao",
	"hwhhzmk":             "Zhang Mingkang",
	"icis":                "Lee Wonyoung",
	"jamass":              "Wi Taewoong",
	"james0716":           "Ding Shaojie",
	"jason1993":           "Cai Jing",
	"jasper92":            "Zhang Jiahuan",
	"jbr":                 "Jian Jingting",
	"jbs360":              "Park Sangjin",
	"jhba0425":            "Park Joonhoon",
	"jingjing":            "Dang Yifei",
	"jingting":            "Hu Yuefeng",
	"just1992":            "Peng Liyao",
	"jyoifuru":            "Nishi Takenobu",
	"karroyjack":          "Zhao Yifei",
	"kawhelio":            "Wu Hao",
	"kkbox":               "Yu Zhengqi",
	"koinoyose":           "Ye Hongyuan",
	"kongm":               "Huang Yunsong",
	"lcs1999":             "Li Chengsen",
    "leaf":                "Shi Yue",
	"lee55":               "Lee Yeongkyu",
	"lee9dan":             "Lee Chungyu",
	"legend8842":          "Yu Lijun",
	"lissome":             "Yao Zhiteng",
	"litlemore":           "Sotoyanagi Sebun",
	"lonelyback":          "Tao Hanwen",
	"lucir96":             "Kim Jinhwi",
	"madongsuk":           "Park Jinsol",
	"maeum":               "Kang Yootaek",
	"maker":               "Park Junghwan",
	"marny":               "Onishi Ryuhei",
	"mengqiuyu":           "Meng Fanxiong",
	"milla517":            "Takashima Yugo",
	"miracle97":           "Byun Sangil",
	"mushroom":            "Xu Zhenyu",
	"myself1":             "Yuan Tingyu",
	"nagatake":            "Seto Taiki",
	"namatya":             "Wu Baiyi",
	"nanairo":             "Seki Koutarou",
	"nesiggu1":            "Han Sangcho",
	"nightraid1":          "Lin Yancheng",
	"noremorse":           "Kim Myounghoon",
	"nparadigm":           "Shin Jinseo",
	"oneokrock":           "Sada Atsushi",
	"onestar":             "On Sojin",
	"onlyyouqaq":          "Zhan Yidian",
	"opening97":           "Choi Hongyun",
	"otowa":               "Motoki Katsuya",
	"pangfeizhu":          "Wang Lei (s)",
	"partofme":            "Li Dongfang",
	"persevere":           "Jiang Qirun",
	"phathos":             "Kim Junseok",
	"physical":            "Choi Jaeyoung",
	"piaojie":             "Kang Dongyun",
	"pms0329":             "Lee Heesung",
	"powerade":            "Kim Hyeongwan",
	"pukino":              "Watanabe Kei",
	"qingkuang":           "Pan Weijian",
	"qiruitian":           "Tian Ruiqi",
	"qkrrjsgh":            "Park Geunho",
	"qoqhan":              "Lin Jiehan",
	"raccoonzs":           "Lin Shixun",
	"revenge":             "Chen Yunong",
	"rkdfkfzld":           "Yang Wooseok",
	"roln":                "Shikshin Ilya",
	"sehgs65":             "Xu Jiayang",
	"sentokun":            "Tanaka Koyu",
	"seobs01":             "Seo Bongsoo",
	"shoxtv":              "Park Jeonggeun",
	"silvers7":            "Ida Atsushi",
	"singlesong":          "Fan Yin",
	"smallpooh":           "Oh Yujin",
	"smile":               "Yang Dingxin",
	"sniperkill":          "Shin Minjun",
	"snowbaby":            "Wu Yiming",
	"steadfast":           "Luo Xihe",
	"stealer":             "Hong Seongji",
	"strict1":             "Huang Xin",
	"summerdive":          "Koyama Kuya",
	"takoyaki":            "Otake Yu",
	"tdcq":                "Li Xiangyu",
	"tiger":               "Yoda Norimoto",
	"tlearn":              "Shibano Toramaru",
	"tmch":                "Choi Woosu",
	"treble":              "Baek Hyeonu",
	"triathlon":           "Liu Yuhang",
	"tuyt":                "Rong Yi",
	"twicett":             "Baek Chanhee",
	"vegetarian":          "Li Haojie",
	"veryeasy":            "Park Jinyoung",
	"wakaba":              "Akiyama Jiro",
	"warriors1":           "Sim Jaeik",
	"waseaya":             "Kobayashi Koichi",
	"watanabe1":           "Watanabe Kouki",
	"william32":           "Chen Shoulian",
	"wlaud":               "Kim Jimyoung",
	"wonfun":              "Weon Seongjin",
	"wujiany":             "Liao Yuanhe",
	"xueGO":               "Zhao Wei",
	"xxzxz222":            "Xu Jiawei",
	"yh7525":              "Heo Yongho",
	"yingyitao":           "Ying Yitao",
	"ykpcx":               "Fan Tingyu",
	"ylbwq":               "Xu Feiran",
	"yubin0202":           "Yu Binghuang",
	"yuuki0523":           "Wang Zhihong",
	"ziggler":             "Xu Yuqi",
	"ziniu":               "Niu Yutian",
	"zxuexue":             "Liu Xi (2)",
	"一叶如秋":                "Yu Qingquan",
	"一条大fish":             "Yu Haoran",
	"一花一天堂":               "Xu Haohong",
	"一骑绝尘8":               "Zeng Yuanhai",
	"三目中林":                "Li Weiqing",
	"丨Taunt丨":             "Guo Xinyi",
	"交易员":                 "Mao Ruilong",
	"以量取胜":                "He Xin",
	"任我行棋":                "Lu Minquan",
	"俩大海归来":               "Chen Junyu",
	"修罗炼狱":                "Wang Zeyu",
	"假想噬界":                "Wang Shuo (00)",
	"傀儡操纵者":               "Ji Xiang",
	"八月二十":                "Ding Mingjun",
	"八月二十一":               "Yang Rundong",
	"内圣外王":                "Wang Zheming",
	"冰冷记忆":                "Fang Hao",
	"冲天一次":                "Cheng Jiaye",
	"凋零玫瑰":                "Xu Yingcai",
	"初雪":                  "Nyu Eiko",
	"剑过无声":                "Lian Xiao",
	"势如破竹1":               "Li Haotong",
	"包子321":               "Zhao Yucai",
	"北海的早晨":               "Fan Yunruo",
	"千寻雨墨":                "Liu Huiling",
	"协鑫集成":                "Ma Tianfang",
	"南小鸟":                 "Jiao Shiwei",
	"危楼高百尺":               "An Dongxu",
	"古剑焚寂":                "Gao Tianliang",
	"只吃蛋白":                "Wang Shuo (00)",
	"向秋森花":                "Wang Lei (b)",
	"命中丿注定":               "Jiang Wei",
	"咆哮":                  "Chen Zijian",
	"囚天01":                "Xue Hongzhe",
	"墨耘":                  "Yu Fei",
	"夕阳的泪痕":               "Hu Aohua",
	"夜黑雨紧":                "Chen Bisen",
	"大名围棋":                "Wang Haoyang",
	"天域之神":                "Shi Yulai",
	"天翔龙闪":                "Tang Chongzhe",
	"天选":                  "Tuo Jiaxi",
	"奇遇心":                 "Zhang Qi",
	"奈文魔尔":                "Chen Yafeng",
	"孔多比亚":                "Liu Jinming",
	"孤星州":                 "Chen Hao (s)",
	"完杀":                  "Liu Qifeng",
	"小狮子宝宝":               "Yuan Yitian",
	"小花像小花":               "Zhan Ying",
	"小菜一碟":                "Cai Wenchi",
	"小香馋猫":                "Chang Hao",
	"尝胆":                  "Li Zerui",
	"峨眉渔樵":                "Tu Xiaoyu",
	"巴黎雨巷":                "Yuan Jie",
	"庄子秋水":                "Lu Liyan",
	"应天飞狐":                "Li Yuang",
	"弈帆风顺":                "Cai Bihan",
	"弑神者":                 "Zheng Yuhang",
	"张森":                  "Zhang Sen",
	"张馨月":                 "Zhang Xinyue",
	"很懒的猫":                "Peng Quan",
	"心神合一":                "Wang Ruoran",
	"思想的星空":               "Zhao Chenyu",
	"恍如隔世":                "Han Enyi",
	"愿我能":                 "Meng Tailing",
	"我想学一盘":               "Ma Qingqing",
	"我是来看我":               "Liu Yuncheng",
	"我有点醉":                "Chen Yang",
	"我来虐菜":                "Li Zehao",
	"拓荒勇士":                "Yan Zaiming",
	"摸连奴":                 "Li Huasong",
	"文兆仪":                 "Wen Zhaoyi",
	"无痕":                  "Yu Zhiying",
	"时修":                  "Gao Yu",
	"时间管理":                "He Yuhan",
	"星之所在":                "Wei Yibo",
	"星宿老仙":                "Gu Li",
	"晨曦战神":                "Zhao Fei",
	"曲子":                  "Wan Leqi",
	"曾经的回忆":               "Li Xuanhao",
	"最好的那年":               "Fang Ruoxi",
	"月冠":                  "Xue Guanhua",
	"机动":                  "Xia Chenkun",
	"杀人执照":                "Cai Wenxin",
	"杨博崴":                 "Yang Bowei",
	"林书豪":                 "Yu Fulin",
	"棋神020137":            "Ma Guangzi",
	"横跨帝国":                "Wang Shiyi",
	"欲望":                  "Han Yizhou",
	"死神永生":                "Zhang Tao",
	"水水雨雨":                "Liu Qinglin",
	"沙小沫":                 "Zhou Yushan",
	"洗心静悟":                "Hu Xiao",
	"浅窗":                  "Wu Zhenyu (s)",
	"浩渺十里亭":               "Shu Yixiao",
	"深圳稻草人":               "Tong Yun",
	"清风与鹿丶":               "Chu Keer",
	"渔岛风":                 "Wang Xinghao",
	"漆黑之牙0":               "Chen Xudong",
	"潘亭宇1":                "Pan Tingyu",
	"潜伏":                  "Ke Jie",
	"潜心者1":                "Zhao Junzhe",
	"澄公":                  "Chen Wenzheng",
	"澳洲小肥羊":               "Yang Zixuan",
	"炫动舞步":                "Wu Jun",
	"炼心":                  "Shi Yue",
	"王元均":                 "Wang Yuanjun",
	"琪琪学棋":                "Wang Jiaqi",
	"琴里":                  "Yin Qu",
	"田鼠宝宝":                "Li He",
	"疯子":                  "Liao Xingwen",
	"白云君":                 "Xie He",
	"白头到老":                "Qiao Zhijian",
	"白露7":                 "Zheng Zijian",
	"看月听雨":                "Yan Huan",
	"知音漫客":                "Luo Yan",
	"破牢":                  "Gui Wenbo",
	"神王崛起":                "Chen Zhengxun",
	"神话傳说":                "Li Xunzheng",
	"神龙之息":                "Wang Shuo",
	"秋天的老虎":               "Chen Yusen",
	"秦棋缘":                 "Qin Jialin",
	"紫塞明珠":                "Jia Yifan",
	"约什杰克逊":               "Chen Yifu",
	"终南山":                 "Song Ronghui",
	"经纬圣斗士":               "Zhao Guanru",
	"网络神":                 "Chen Hao",
	"美国大总统":               "Huang Chunqi",
	"胖铭铭":                 "Li Ming",
	"胜负师":                 "Yu Zhengqi",
	"臭的不行":                "Wang Ziang",
	"舞动de灵魂":              "Hou Jingzhe",
	"艾斯德斯":                "Huang Jingyuan",
	"若只如初见":               "Sun Li",
	"荆轲刺秦王":               "Zhang Junzhe",
	"荼毒众生":                "Shi Ji",
	"蓼蓝":                  "Zhang Tiange",
	"蕭正浩":                 "Xiao Zhenghao",
	"血色风凌":                "Yi Lingtao",
	"词化":                  "Hang Xiaotong",
	"语嫣m":                 "Gao Youtong",
	"诸神的荣耀":               "Tang Weixing",
	"谜团":                  "Chen Yaoye",
	"质直若神":                "Yang Wenkai",
	"车站1997":              "Pan Yang",
	"达尔文":                 "Tong Yulin",
	"还我河山":                "Liu Yuhang",
	"这也太迷了":               "Kou Zhengyan",
	"逆袭丿暴走":               "Guo Yuzheng",
	"逍遥无梦":                "Wang Wei",
	"逝去的孤影":               "Chen Xian",
	"道是心常平":               "Wu Guangya",
	"道隐因本心":               "Wang Xiangru",
	"那天的傍晚":               "Yang Zongyu",
	"醉意朝东":                "Cheng Honghao",
	"铃木旋风雄":               "Chen Xiaotian",
	"长行莫围qi":              "Li Xinyi",
	"阿法熊丞丞":               "Jin Yucheng",
	"阿赖耶识03":              "Zhao Zhongxuan",
	"陳鋒":                  "Chen Feng",
	"陳首廉":                 "Chen Shoulian",
	"隐忍黑衣人":               "Feng Yi",
	"雅塔雷斯":                "Shen Peiran",
	"雪域青莲":                "Zhou Hongyu",
	"雪融奔海去":               "Zhang Chi",
	"霍华德":                 "Hua Chang",
	"霸dao":                "Wang Xi",
	"韩笑天下":                "Qian Liuru",
	"風起":                  "Li Wei",
	"风灵之声":                "Huang Mingyu",
	"风烟俱尽":                "Zheng Zaixiang",
	"魔法之风":                "Jiang Chenzhong",
	"魔術":                  "Huang Shiyuan",
	"鸟生鱼汤":                "Ma Xiaobing",
	"龙门阵":                 "Gu Lingyi",
}

known_players = dict()		# Constructed later from the raw data above. Will be lowercase keys only.


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

				if new_string == "3.25":		# Convert Chinese komi notation, if present.
					new_string = "6.5"
				if new_string == "3.75":
					new_string = "7.5"

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
			regex_PB, regex_PW = re.search(r"\[(.+)\]vs\[(.+)\]\d+.sgf", filename).group(1, 2)
		except:
			pass

		if regex_PB and regex_PB.lower() in known_players:
			black_real_name = known_players[regex_PB.lower()]
			root.safe_commit("PB", "{} ({})".format(regex_PB, black_real_name))
		elif PB and PB.lower() in known_players:
			black_real_name = known_players[PB.lower()]
			root.safe_commit("PB", "{} ({})".format(PB, black_real_name))

		if regex_PW and regex_PW.lower() in known_players:
			white_real_name = known_players[regex_PW.lower()]
			root.safe_commit("PW", "{} ({})".format(regex_PW, white_real_name))
		elif PW and PW.lower() in known_players:
			white_real_name = known_players[PW.lower()]
			root.safe_commit("PW", "{} ({})".format(PW, white_real_name))

		black_for_filename = black_real_name if black_real_name else regex_PB if regex_PB else PB if PB else "Unknown"
		white_for_filename = white_real_name if white_real_name else regex_PW if regex_PW else PW if PW else "Unknown"

		# (Done)

		dt = root.get_value("DT")

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


def fix_known_players():
	global known_players_raw
	global known_players

	for key in known_players_raw:
		known_players[key.lower()] = known_players_raw[key]


def main():

	if len(sys.argv) == 1:
		print("Need argument")
		sys.exit()

	fix_known_players()

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

# coding: utf-8
#
# pixivpy_wrapper to nijiflow data file format
#  https://github.com/fallthrough/nijiflow
#

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)
import logging
import PIL.Image

import sys
import os
import os.path


argvs = sys.argv
argc = len(argvs)

if (argc != 4):
	sys.stderr.write('Usage: # python %s class_id dir_path exclude_tags\n' % argvs[0])
	quit()

# 変数作成
# クラス番号(nijiflowファイルに書き込む)
class_id = argvs[1]
# ディレクトリパス
dir_path = argvs[2]
# 使用する画像の最大数(画像数が未満の場合はすべて使う)
image_num = 6500
#image_num = 20000
# 使用する画像から除外するタグ
exclude_tags = argvs[3].split(",")
#exclude_tags = ["アズレン", "アズールレーン"]
#exclude_tags = ["艦これ", "戦艦これくしょん"]


data_file = os.path.join(dir_path, "data.json")
f = open(data_file, 'r')
s = f.read()
#pp.pprint(s)
s = s[:-2]
s = "[\n" + s + "\n]"
#pp.pprint(s)
datas = json.loads(s)
#pp.pprint(datas)
pp.pprint(len(datas))
f.close()

dst_dir_path = os.path.join(dir_path, "nijiflow_data")
os.makedirs(dst_dir_path, exist_ok=True)

nijiflow_file = os.path.join(dst_dir_path, "nijiflow.list")
f = open(nijiflow_file, 'w')

c = 0
for i, data in enumerate(datas):
	if (image_num <= c):
		print("success %d image.(%d)" % (image_num, i))
		break

	#print("%d" % (data['id']))
	if data["type"] != "illustration":
		continue

	if data["page_count"] != 1:
		continue

	for exclude_tag in exclude_tags:
		if exclude_tag in data['tags']:
			print("%d exclude:`%s`" % (data['id'], exclude_tag))
			continue

	image_filename = os.path.basename(data['image_urls']['large'])

	name, ext = os.path.splitext(image_filename)
	if ".jpg" != ext:
		continue

	image_filepath = os.path.join(dir_path, image_filename)
	try:
		image = PIL.Image.open(image_filepath)
	except Exception:
		logging.exception('Failed to open: %s', image_filepath)
		continue
	if image.mode != 'RGB':
		logging.warning('Skipping %s mode image: %s', image.mode, image_filepath)
		continue

	dst_image_filepath = os.path.join(dst_dir_path, image_filename)
	#if not os.path.exists(dst_image_filepath):
	image.resize((224, 224))
	image.save(dst_image_filepath)

	#print("%s" % (image_filepath), flush=True)
	f.write("%s %s\n" % (image_filename, class_id))
	c += 1

	if 0 == (c % 100):
		print("%4d/%4d." % (c, image_num))


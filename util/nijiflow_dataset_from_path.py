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
# ** クラス番号(nijiflowファイルに書き込む)
class_id = argvs[1]
# ** ディレクトリパス
dir_path = argvs[2]
# ** 使用する画像の最大数(画像数が未満の場合はすべて使う)
image_num = 3000
#image_num = 20000
# ** 使用する画像から除外するタグ
exclude_tags = argvs[3].split(",")
#exclude_tags = ["アズレン", "アズールレーン"]
#exclude_tags = ["艦これ", "戦艦これくしょん"]
# ** 画像をあらかじめリサイズ
is_resize_image = False
# ** より評価の高い画像のみを集めたい場合はこの閾値を変更する (ex. 1000, 4000, 10000)
min_score = 0



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

	if data["stats"]["score"] < min_score:
		continue

	for exclude_tag in exclude_tags:
		if exclude_tag in data['tags']:
			print("%d exclude:`%s`" % (data['id'], exclude_tag))
			continue

	image_filename = os.path.basename(data['image_urls']['large'])

	image_filepath = os.path.join(dir_path, image_filename)

	if not os.path.isfile(image_filepath):
		continue

	try:
		image = PIL.Image.open(image_filepath)
	except Exception:
		logging.exception('Failed to open: %s', image_filepath)
		continue

	name, ext = os.path.splitext(image_filename)
	dst_image_filepath = os.path.join(dst_dir_path, name + ".jpg")
	#if not os.path.exists(dst_image_filepath):

	if not is_resize_image:
		if image.mode != 'RGB':
			continue
		if ext != '.jpg':
			image.save(dst_image_filepath)
			image_filepath = dst_image_filepath
	else:
		try:
			dst_image = image.resize((224, 224))
			if dst_image.mode == 'RGB':
				pass
			elif dst_image.mode == 'RGBA':
				#dst_image.convert("RGB")
				tmp_dst_image = PIL.Image.new("RGB", (224, 224), (255, 255, 255))
				tmp_dst_image.paste(dst_image, mask=dst_image.split()[3]) # 3 is the alpha channel
				dst_image = tmp_dst_image
			else:
				#logging.exception('skip: %s %s', image_filepath, dst_image.mode)
				continue

			dst_image.save(dst_image_filepath)
			image_filepath = dst_image_filepath
		except Exception:
			logging.exception('Failed to convert: %s', image_filepath)
			continue

	#print("%s" % (image_filepath), flush=True)
	f.write("%s %s\n" % (image_filepath, class_id))
	c += 1

	if 0 == (c % 100):
		print("%4d/%4d." % (c, image_num))


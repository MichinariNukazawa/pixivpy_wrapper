# coding: utf-8

from pixivpy3 import *

import os
import sys
import argparse
import json
from time import sleep

import pprint
pp = pprint.PrettyPrinter(indent=4)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("tagname")
	parser.add_argument("output_dir")
	parsed = parser.parse_args()


	# 変数作成
	# 検索するタグ
	tagname = parsed.tagname
	# 画像およびデータを保存するディレクトリのパス
	saving_dirpath = "{}_{}".format(os.path.normpath(parsed.output_dir), tagname)
	# 画像データの保存ファイルパス ( @Notice 書き出しは厳密なJSONフォーマットではないので読むときは良いようにする必要がある)
	datafile = os.path.join(saving_dirpath, "data.json")
	# より評価の高い画像のみを集めたい場合はこの閾値を変更する (ex. 1000, 4000, 10000)
	min_score = 0
	# ページ数(x30枚がマッチ)(1000ページ(1~999?)まで)(合計20000画像まで？)
	page_start = 1
	page_num = 2

	# 画像ダウンロードの間隔
	sleep_sec = 1
	# 検索のページ毎の間隔
	if 10 > page_num:
		page_sleep_sec = 0.1
	else:
		page_sleep_sec = 1

	#separator = '------------------------------------------------------------'


	# ログイン処理
	api = PixivAPI()
	f = open('client.json', 'r')
	client_info = json.load(f)
	f.close()
	api.login(client_info['pixiv_id'], client_info['password'])


	# 画像の保存先(なければディレクトリを作成)
	os.makedirs(saving_dirpath, exist_ok=True)


	aapi = AppPixivAPI()

	for page in range(page_start, page_start + page_num):
		sleep(page_sleep_sec)
		#print("[%3d:%d]" % (page, page_num))

		# exact_tag: タグに正確にマッチ(キーワードが１つのみの場合)
		# tag: タグにマッチ(キーワードが1つ以上の場合)
		if 1 == len(tagname.split(' ')):
			json_result = api.search_works(tagname, page=page, mode='exact_tag')
		else:
			json_result = api.search_works(tagname, page=page, mode='tag')
		#illust = json_result.response[0]

		# このキーがある場合は検索に失敗
		if 'has_error' in json_result:
			sys.stderr.write('Error: search error `%s`\n' % (tagname))
			pp.pprint(json_result)
			quit()

		if (not 'response' in json_result) or 0 == len(json_result.response):
			if(1 == page):
				sys.stderr.write('Error: tag not match `%s`\n' % (tagname))
			else:
				print('Notice: tag not match `%s`' % (tagname))
			quit()

		illust_i = -1
		illust_num = len(json_result.response)
		#print("[%3d:%d] tag:`%s` match:%d" % (page, page_num, tagname, illust_num))

		for illust in json_result.response:
			illust_i += 1
			score = illust.stats.score
			if score < min_score:
				continue

			imagefilename = os.path.basename(illust.image_urls['large'])
			imagefile = os.path.join(saving_dirpath, imagefilename)
			if os.path.exists(imagefile):
				sys.stderr.write("Notice: already exist [%3d:%d, %4d:%d] `%s`\n" % (page, page_num, illust_i, illust_num, illust.title))
				sys.stderr.flush()
				continue

			with open(datafile, "a") as f:	# a:追記
				text = json.dumps(illust, indent=2, ensure_ascii=False)
				f.write(text)
				f.write(",\n")
				f.flush()

			print("[%3d:%d, %4d:%d] `%s`" % (page, page_num, illust_i, illust_num, illust.title), flush=True)
			aapi.download(illust.image_urls.large, path=saving_dirpath)
			sleep(sleep_sec)
			#aapi.download(illust.image_urls.large, path=saving_dirpath, name=imagefilename)

if __name__ == '__main__':
	main()


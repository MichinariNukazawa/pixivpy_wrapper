Download images from tag of pixiv
====
[pixivpy]( https://github.com/upbit/pixivpy )を用いて、pixivから指定タグの画像をダウンロードする  


# 免責事項
- 使用する場合は自己責任です。  


# About
ダウンロード済み画像を(画像ファイル名を元に)スキップする程度に[pixivpy]( https://github.com/upbit/pixivpy )をラップしたダウンロードバッチ。  
検索時に取得される画像のデータを、後から使えるようとりあえずJSON(のようなもの)で書き出して残すこともする。  


# Usage
## Install
`sudo apt install python3-pip`  
`pip3 install pixivpy`  


## Account
キーなど、アカウントへアクセスするための固有の情報を書いた`client.json`を、実行時のカレントディレクトリに配置する。  
``` : client.json (example)
{
	"pixiv_id": "hoge@example.com",
	"password": "********"
}
```


## Run
`bash kancolle.sh`  


# References
http://www.mathgram.xyz/entry/scraping/pixiv  



url=`python ./serverless/geturl.py $TENCENT_SECRET_ID $TENCENT_SECRET_KEY`;
if [ -n "$url" ]; then
	wget --no-check-certificate -O code.zip "$url";
	echo "已下载代码文件";
	sudo apt install -y unzip;
	unzip -o code.zip -d code/;
	rm -f code.zip;
	sudo mv ./code/config.json ./oldconfig.json;
	python ./serverless/loadconfig.py;
	echo "已加载配置文件";
else
	echo "未获取到下载链接，如已部署，配置将被覆盖";
fi
echo "开始安装ServerlessFramework";
sudo npm install -g serverless;
sudo mkdir tmp/;
shopt -s extglob;
sudo mv !(tmp|serverless|code|.github|.git) ./tmp;
sudo mv ./serverless/serverless.yml ./tmp;

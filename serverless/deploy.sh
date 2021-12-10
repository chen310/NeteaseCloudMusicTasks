if [ -n "$FUNCTION_NAME" ]; then
	arg_fn="$FUNCTION_NAME"
else
	arg_fn="NeteaseCloudMusicTasks"
fi
if [ -n "$REGION" ]; then
	arg_region="$REGION"
else
	arg_region="ap-guangzhou"
fi
url=`python ./serverless/geturl.py $TENCENT_SECRET_ID $TENCENT_SECRET_KEY $arg_fn $arg_region`;
if [ -n "$url" ]; then
	echo "正在下载代码文件";
	wget --no-check-certificate -q -O code.zip "$url";
	echo "已下载代码文件";
	sudo apt install -y unzip  >> /dev/null;
	echo "正在解压"
	unzip -o code.zip -d code/  >> /dev/null;
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
sudo mv !(tmp|serverless|public|code|.github|.git) ./tmp;
sudo mv ./serverless/serverless.yml ./tmp;

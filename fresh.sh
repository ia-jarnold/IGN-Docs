# rebuilds and deploys ign-docs
docker stop ign-docs
docker rm ign-docs
docker image rm ign-docs
docker build -t ign-docs .
docker run --name ign-docs \
	-p 5000:5000 \
	-v /home/jarnold/Projects/IGN-Docs/docs/source:/app/docs/source \
	-v /home/jarnold/Projects/IGN-Docs/logs:/app/logs \
	--restart always \
	-d ign-docs 

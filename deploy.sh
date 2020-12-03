docker build -t anandrajaram21/covid-19:prod -f prod.Dockerfile .
docker run -it --rm -p 8050:8050 anandrajaram21/covid-19:prod

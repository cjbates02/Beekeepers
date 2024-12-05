# build docker image for amd64 architecture because i am developing on a m1 mac which uses arm
docker login
docker buildx build --platform linux/amd64 -t cjbates02/beekeeper-ui:latest .
docker push cjbates02/beekeeper-ui:latest

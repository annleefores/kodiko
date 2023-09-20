# build and push codepod-build
docker build -f build.Dockerfile -t annleefores/codepod-build:1.0.0 . \
&& docker push annleefores/codepod-build:1.0.0

# build and push codepod-deploy
docker build -f deploy.Dockerfile -t annleefores/codepod-deploy:1.0.0 . \
&& docker push annleefores/codepod-deploy:1.0.0



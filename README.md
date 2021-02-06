# A.N.U. Website & Dashboard

server/
- launch-dev.sh <-- contains pre and post deploy scripts when running app locally
- Procfile <-- contains docker image deploy run script
- app.json <--contains pre-deploy scripts to run once container image is built

frontend/
- npm run start:dev
- npm run build 
- etc...

hooks/
- pre-build <-- contains scripts which will run on the dokku host before building docker image
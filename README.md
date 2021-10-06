# A.N.U. Website & Dashboard

**server/**
- `python manage.py test`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py collectstatic`
- `python manage.py createsuperuser`
- `gunicorn config.wsgi -b 0.0.0.0:8000 --workers=2 --threads 2 --reload`

**frontend/**
- `npm run test:unit`
- `npm run start:dev`
- `npm run build` 

**Docker**
- `docker-compose.yml` <-- for local deploy only
- `Dockerfile` <-- for dokku deploy

- `launch-dev.sh` <-- contains pre and post deploy scripts when running app locally
- `Procfile` <-- contains docker image deploy run script
- `app.json` <--contains pre-deploy scripts to run once container image is built

**Docker development environment**
- run `docker compose up` in root dir to start `server`, `frontend` and postgres `db`
- run `docker-compose down` to stop everything

**Dokku**
- add dokku server to your git remote then push repo to deploy

**ENV vars**
- `AWS_ACCESS_KEY_ID=your-storage-access-key-id`
- `AWS_SECRET_ACCESS_KEY=your-storage-access-key`
- `AWS_STORAGE_BUCKET_NAME=your-storage-container-name`
- `LINODE_PAT=your-linode-pat-key`
- `MAX_LINODES=1`

**jacktrip-server-automation API**
For local testing this requires deploy scripts to be manually placed in the root directory at `jacktrip-server-automation/` there should
be an entry point named `jacktrip-server-automation/scripts/install.sh`.
For deployment on dokku you should put these same scripts in `/var/lib/dokku/data/storage/anu-website/jacktrip-server-automation/` where it will be
mounted in a volume on the docker container.
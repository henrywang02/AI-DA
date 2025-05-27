- [Project info](#project-info)
	- [Current Capabilities](#current-capabilities)
		- [FastAPI](#fastapi)
		- [React UI](#react-ui)
	- [Future improvements](#future-improvements)
	- [Production environment setup guide](#production-environment-setup-guide)
	- [Development environment setup guide](#development-environment-setup-guide)
		- [FastAPI backend](#fastapi-backend)
		- [React Frontend](#react-frontend)


> HUA TRUNG HIEU's approach for the deployment can be found on [./phase_6_result.ipynb](./phase_6_result.ipynb).

> A little more experimentation was done with the phase 4 which can be seen from [./train/phase_4_results_retrain.ipynb](./train/phase_4_results_retrain.ipynb) file.

# Project info

This project is separated in two parts UI and API for development ease. These are:
1. FastAPI backend serves the HTTP endpoints to get the predictions, add new data and retrain models.
2. React UI which communicates with the FastAPI to handle the user interaction.

> Current implemented functionalities of the API's and UI can be seen by running the project with docker following the steps in the [production](#production-environment-setup-guide) or [development](#development-environment-setup-guide).

## Current Capabilities

### FastAPI
1. Get price predictions
2. Add new data rows
3. Get label mappings
4. Retrain models with combined datasets

### React UI
1. Enter data and get predictions for price
2. Add new data row with `X`(feature) and `Y`(target) columns which will help getting more accuracy
3. Call retrain_models endpoint using a button

## Future improvements
1. Make the UI look nice. Show retraining progress on the UI. Can be done using `long polling` or `websocket`.
1. Mount dynamic files which can be useful for later like `logs` and `inserted data` vai api endpoints to the host os using docker's mount points in a directory under the project's directory. For example `docs/Phase 6/mount_points/fastAPI/` and `docs/Phase 6/mount_points/nginx/`, otherwise these dynamic data will be lost when a container crashes or system reboots.
2. Implement a way to serve multiple versions of models like: LRv1.1, LRv2.2, XGBv1.2, XGBv2.1, ..., etc. along with the metrics so users can decide which one to use.
3. Schedule the retraining of models using additional data. Can be done with `systemd` or `crontab`
4. And of course creating prediction models for other things like predicting how many days a car will be on market to make better decisions to make profits.




## Production environment setup guide
This project is set up to run in production using docker, which will handle restarts when the host machine reboots or the containers crashes in case of errors.

Requirements:
1. A VPS with Linux OS
2. Docker daemon and cli installed on the

> Info: In the production nginx handle all the incoming requests and forwards any request going to `/api/*` / `/docs/*` / `/openapi.json` to the FastAPI backend. And other requests are assumed to be for the static files which nginx serves from the artifacts of `npm run build` command. If the resource for those request not found nginx will simply reply with HTTP 404 status code to indicate file not found error.

Steps to run the server:
1. Transfer all the files of `docs/Phase 6/` directory or clone the repository to the Linux Server via any means(eg. SSH, FTP, etc.)
2. Before running the following steps the `working directory` or `pwd` should be `docs/Phase 6/` or where the the contents of the `Phase 6` were copied
3. `docker compose up -d` this will build the images and run the two containers
4. Now, you can visit `http://{server_ip}:80` to see the UI and interact with it using any web browser.
5. Logs can be seen using docker command.
6. Nginx specific logs like error/access logs can be seen via connecting shell to the nginx container using docker.


> Note: System admin should take measure and set up firewall rules after setting up the server. This is out of the scope of this Project so I am not going to discuss about security here.


## Development environment setup guide

### FastAPI backend

1. Install anaconda to manage python environment
3. `conda create -n aida python=3.12` creates conda environment for the project
4. `conda activate aida` activates the created environment
5. Before running the following steps the `working directory` or `pwd` should be `docs/Phase 6/api`
6. `pip install -r requirements.txt` instals the required packages for the project
7. `fastapi dev` runs the API and reloads the server when files changes in the app directory
8. Now, you can visit `http://localhost:8000` to see the API endpoints and try out the endpoints


### React Frontend

1. Before running the following steps the `working directory` or `pwd` should be `docs/Phase 6/ui`
2. Note: During the development the `node:22` version was used, so keeping the same version will avoid unexpected errors
3. `npm install` will install the node packages
4. `npm run dev` will run the vite server for the UI with HMR
5. Since the FastAPI is begin ran on port `8000` you will have to update the `BASE_URL` in [`docs\Phase 6\ui\src\services\api.ts`](https://gitlab.labranet.jamk.fi/AC4933/aida-project-spring-2025/-/blob/master/docs/Phase%206/ui/src/services/api.ts#L6) file accordingly.
6. Now, you can visit `http://localhost:5173` to see the UI and interact with it.

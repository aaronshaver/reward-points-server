# reward-points-server

REST API server which records transactions, keeps track of points, allows point
spending

## Server installation

1. Install Docker if it doesn't exist on your local machine. This will ensure
 the same dependencies as when the app was developed. Download here:
https://www.docker.com/get-started/
1. On the terminal, clone this repository you're in now
 (`git clone git@github.com:aaronshaver/reward-points-server.git`) while in a
 local directory on your machine
1. `cd` into the new directory, e.g. `cd reward-points-server`
1. `docker build -t rewardpoints .`

## Server usage

1. Run server: `docker run -p 80:80 rewardpoints`
1. Send REST API requests to the server: see section below
1. Run unit tests: without starting the container (i.e. outside the container on
your localhost with Python 3 installed): `python3 -m unittest discover app/.`
1. If for some reason the unit tests won't work on your environment, you can
command out (with # hash sign) the CMD line in the Dockerfile, rebuild the image
and then do: `docker run -it rewardpoints /bin/bash` to run them inside the
 pristine Docker environment
1. View the generated API docs: `http://localhost/docs`

## API usage

Postman examples...

## Design considerations

to be done...
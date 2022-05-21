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
1. Send REST API requests to the server: see API Usage below
1. Run unit tests: without starting the container (i.e. outside the container on
your localhost with Python 3 installed): `python3 -m unittest discover app/.`
1. If for some reason the unit tests won't work on your environment, you can
comment out (with `#` hash sign) the CMD line in the Dockerfile, rebuild the image
and then do: `docker run -it rewardpoints /bin/bash` to run them inside the
 pristine Docker environment
1. View the generated API docs: `http://localhost/docs`

## API usage

1. Use the API like a standard HTTP REST web server. For example, you can
install Postman and create a user by sending a POST to `localhost/users/new` as
 long as the container is running using the steps above.

## Design considerations

* I hadn't used FastAPI before (I used to use Flask), but I read it was a great
 new REST framework so I decided to learn it
* It didn't feel right not having users in the system, so I implemented
 rudimentary user creation/retrieval logic
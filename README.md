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

Use the API like a standard HTTP REST web server. For example, you can
install Postman and use it to do requests.

Workflow example:

1. create a user by sending a POST to `localhost/users` (make sure the
 container is running first, using the steps above!)
1. ....................
1. ....................

## Design considerations

* I hadn't used FastAPI before (I used to use Flask), but I read it was a great
 new REST framework so I decided to learn it
* It didn't feel right not having users in the system, so I implemented
 rudimentary user creation/retrieval logic. This came in handy when doing manual
 integration testing in Postman: I could get a fresh environment by simply
 creating a new user instead of restarting the whole server.
* Initially I thought the problem was simple enough, and I'd try to keep things
 simple by using plain Python objects for everything. Partway through, I
 realized using a database (even something lightweight like SQLite) and a basic
 ORM would have made things MUCH easier, particularly sorting and filtering
 transactions. It would be a case of "use slightly more tooling and make
 infrastructure slightly more complicated to get big gains in developer
 efficiency".
* If I did this project over again, I would do it using a database. It would be
really nice to be able to use SQL to do stuff like: `SELECT SUM(points) FROM
 transactions WHERE payer_id = 1 AND user_id = 'uuid' ORDER BY timestamp`
* The exercise document didn't specify what to do in case of trying to spend
 more points than were available for the user, so I went with the conservative
 approach of not allowing that kind of spend request to succeed (you'll get a
 400 bad request and points will remain unspent if you try)
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
1. Send REST API requests to the server: see `API usage / workflow example`
 below
1. Run unit tests: without starting the container (i.e. outside the container on
your localhost with Python 3 installed): `python3 -m unittest discover app/.`
1. If for some reason the unit tests won't work on your environment, you can
comment out (with `#` hash sign) that last CMD line in the Dockerfile, rebuild
the image and then do: `docker run -it rewardpoints /bin/bash` to run them
inside the pristine Docker environment
1. View the generated API docs: `http://localhost/docs`

## API usage / workflow example

Use the API like a standard HTTP REST web server. For example, you can
install Postman and use it to do requests. (Just make sure the container is
running first, using the steps above!)

1. create a user: POST to `localhost/users`; take note of the `user_id` returned
1. add a transaction: POST to `localhost/users/{{user_id}}/transactions` with
request body:
 `{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }`
 (you'll need to put the user_id in the path, replacing {{user_id}})
1. spend points: POST to `localhost/users/{{user_id}}/points` with request body
 `{ "points": 1000 }`
1. get current point totals: GET from `localhost/users/{{user_id}}/points`

If `localhost` doesn't work, your platform may need something different, like
 `127.0.0.1`. Please consult your REST API client documentation as needed.

## Design considerations

* It didn't feel right not having users in the system, so I implemented
 rudimentary user creation/retrieval logic. This came in handy when doing manual
 integration testing in Postman: I could get a fresh environment by simply
 creating a new user instead of restarting the whole server. So the solution is
 a super-set of the exercise instructions (i.e. it'll do everything required of
 the instructions plus be able to handle multiple users)
* Initially I thought the problem was simple enough, and I'd try to keep things
 simple by using plain Python objects for everything. Partway through, I
 realized using a database (even something lightweight like SQLite) and a basic
 ORM would have made things MUCH easier, particularly sorting and filtering
 transactions. It would be a case of "use slightly more tooling and make
 infrastructure slightly more complicated to get big gains in developer
 efficiency". If I did this project over again, I would do it using a database.
 It would be really nice to be able to use SQL to do stuff like: `SELECT SUM(points) FROM
 transactions WHERE payer_id = 1 AND user_id = 'uuid' ORDER BY timestamp`
* The exercise document didn't specify what to do in case of trying to spend
 more points than were available for the user, so I went with the conservative
 approach of not allowing that kind of spend request to succeed (you'll get a
 400 bad request and points will remain unspent if you try)
* The implementation code for the
 `@app.post("/users/{user_id}/points", status_code=200)` route is pretty long,
 I know. I would like to refactor it, but I've simply run out of the time I
 allocated for this code challenge.
* I wanted to do an immutable "Ledger" storage too, which you could use for
 debugging, compliance, etc. but I did not have time.
* I have some error handling, but in a production quality app I would add even
 more, e.g. handle payer names with different lower and upper cases
* I hadn't used FastAPI before (I used to use Flask), but I read it was a great
 new REST framework so I decided to learn it
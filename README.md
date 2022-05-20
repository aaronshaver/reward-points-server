# reward-points-server

REST API server which records transactions, keeps track of points, allows point
spending

## Installation

1. Install Docker if it doesn't exist on your local machine. This will ensure
 the same dependencies as when the app was developed. Download here:
https://www.docker.com/get-started/
1. On the terminal, clone this repository you're in now
 (`git clone git@github.com:aaronshaver/reward-points-server.git`) while in a
 local directory on your machine
1. `cd` into the new directory, e.g. `cd reward-points-server`
1. `docker build -t rewardpoints .`
1. `docker container run -it rewardpoints /bin/bash`

## Usage

1. Run server: `python3 application.py sample_drivers.txt sample_destinations.txt`
1. Run unit tests: `python3 -m unittest discover .`

## Design considerations

to be done...
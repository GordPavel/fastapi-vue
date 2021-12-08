# Equations solver

### Contents

The [frontend folder](services/frontend) contains vue SPA, that uses
[backend](services/backend) to calculate equations. Backend works on python with 
numpy and matplotlib dependencies.
Now there is just 1 equations solver: quadratic. If you want, you can contribute your 
own solvers with web from for them.

## Want to use this project?

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

After this run check http://localhost:8080/, backend endpoints are available
on http://localhost:8000/

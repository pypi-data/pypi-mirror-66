# Daltons

Daltons is a contextual bandit based reinforcement learning service.

## Running

### With docker (single policy model)
```sh
$ docker run gcr.io/unity-ads-common-prd/daltons:latest decision-service
```

### From source (single policy mode)

```sh
$ go run main.go decision-service
```

### Install (single policy mode)

```sh
$ go install .
$ daltons decision-service
```

After Daltons has started you can visit http://localhost:8080/swagger-ui/ for the swagger UI. 


### Setting up separate admin, decision service and trainer process (multi policy mode)

Running separate decision service(s) and trainer process allows us to balance inference into multiple decision services while still training a single model on a single trainer process.

*First install Daltons*

`go install github.com/Applifier/daltons`

*Create a temporary folder for the models*

```sh
mkdir .temp/
```

*Start redis server (or nats or kafka or pubsub)*

```sh
$ redis-server
```

*Start admin / policy management service*

```sh
$ daltons admin -s "file://$PWD/.temp" -g ":8091" -p ":8090" -u "your-user" -P "passw0rd"
```
- `-s "file://$PWD/.temp""` point the service to load policies from ./temp directory
- `-g ":8091"` defines GRPC port
- `-p ":8090"` defines HTTP port
- `-u "your-user"` and `-P "passw0rd"` defines a username and password to protect the admin service

*Start decision-service*

```sh
$ daltons decision-service -t=false -l="pms://localhost:8091?update_interval=5s" -e="redis://"
```

- `-t=false` disable in process background trainer (we have a separate process for that)
- `-l="pms://localhost:8091?update_interval=5s"` point the service to load policies from PMS every 5s
- `-e="redis://"` define example lods to be pushed to a redis pubsub topic (these are used for training)

*Start trainer*

```sh
$ daltons trainer -d="redis://" -t="pms://localhost:8091"
```
- `-d="redis://"` dataset to be read for learning (redis where we are pushing the logged examples)
- `-t="pms://localhost:8091"` where to load policy configurations (PMS).

*Run example predictions*

```sh
$ go run examples/drinkpredictor/main.go
```

## Usage

See [api docs](docs/protobuf.md#decisionservice) or [clients](clients/) for usage examples 

### Clients

- [Golang](clients/go/)
- [Javascript/NodeJS](clients/js/)
- [Python](clients/python/)

# Components

## Eventhub(s) (pkg/internal/eventhub)

- Implements decisionservice.EventLogger
- Used to log Examples (information for RankRequest or Backfill), Actions (activations of action) and Outcomes
- Implementations for multiple different targets (inmem, redis, pubsub etc.)
- Logged events are used to either join rank calls, action activations and outcomes together or by using backfilled examples to create a Dataset for learning.

## Dataset(s) (pkg/internal/eventhub/redis, pkg/internal/eventhub/inmem, pkg/internal/example/tfexample)

- Implements learn.DatasetIterator
- Used for training a model using learn.Learn function that takes in a DatasetIterator and the learn.Model to be trained
- Implementations for multiple different sources (inmem, redis, file etc.) and for different formats

## Loader (internal/pkg/loader)

- Implements decisionservice.ModelLoader
- Returns models to DecisionService to be used for Rank requests
- Instantiates policy type (vw, pytorch, tensorflow) specific policy loaders
- Check for Policy configuration changes to re-load model specific loaders
- Model type agnostic (model type specific policy creator is implemented separately)

### Vowpal Wabbit loader.PolicyCreator (internal/pkg/algos/vowpal/loadercreator.go)

- Implements loader.PolicyCreator for Vowpal Wabbit (vw) policies
- Loads models for the policy
- Handles AB testing for different models configured for the policy

## Trainer (internal/pkg/trainer)

- Implements learn.Model
- Used to train policies based on policy configurations
- Can automatically create new policies if new policy ids are found from the learning dataset
- Model type agnostic (model type specific policy creator is implemented separately)

### Vowpal Wabbit trainer.PolicyCreator (internal/pkg/algos/vowpal/trainercreator.go)

- Implements trainer.PolicyCreator for Vowpal Wabbit (vw) policies
- Instantiates models configured for the policy
- Uploads models every configured example limit or in specified time intervals

## Re-generating proto, docs, swagger clients etc.

```sh
$ cd tools && docker-compose run gen
```

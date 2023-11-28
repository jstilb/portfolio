# askwiki backend

This directory contains all code necessary to run our app's backend.

Installation is slightly different on the prod (AWS) box: we need to add "sudo" before some
commands.

## Release notes (2/16):

* At present, the AWS box exposes port 8000 for http (NOT https) and there is no authentication
of any kind, so anyone on internet that knows the url (unlikely) can hit the api
* I have been stopping and starting the AWS box, so the URL of the instance changes every time.
* This is version 0 that has only a dummy pipeline.
* Model packaging is TBD
* In all commands below, `sudo` should only be necessary on the prod AWS box

## Running the backend service

To start the backend service, cd into `kgqa-ucb-210/backend` and run this command:
```
sudo ./run.sh
```
That command will:
* rebuild the docker image if necessary
* stop the currently running service if there is one
* start the service
* run a few health and sanity checks
* tail and follow the logs

If you ctr-c out of the log tailing
the service will continue to run in the background. If you need to stop the service, run
```
sudo docker stop askwiki
```

## API Summary

In the examples below, I assume there is a shell variable set up something like this:
```
export ASKWIKI_HOST=localhost
```
or, for the prod service,
```
export ASKWIKI_HOST=54.245.102.169
```

### Health Check

Check health as follows:
```
curl "http://$ASKWIKI_HOST:8000/health"
```
That should return:
```
{"status":"healthy"}
```

### The "ask" api

This curl command illustrates the input to the ask api. Note that it uses POST.

```
curl -X POST "http://$ASKWIKI_HOST:8000/ask/" \
   -H 'Content-Type: application/json' \
   -d '{"pipeline": "dummy", "question": "what is the difference between a duck?"}'
```
The response from the dummy pipeline should be (formatted for readability):
```
{
  "pipeline": "dummy",
  "question": "what is the difference between a duck?",
  "sparql": "this is supposed to be a sparql query",
  "rawresults": "this is supposed to be sparql query results",
  "summary": "this is supposed to be a summary"
}
```

The dummy pipeline echoes back the `pipeline` and `question` parameters, and adds:
* `sparql` - this should be the real translated sparql
* `rawresults` - this should be the results from the sparql query, as a table
* `summary` - this should be the summary

## Testing


To run the tests, cd into `backend/askwiki` and run `poetry run pytest`.

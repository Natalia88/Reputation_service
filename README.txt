# Reputation Service

A simple microservice for calculating reputation based on hash strings
using workers and task queue and dummy analyzer.


## Overview

The service receives a hash string, creates task for a worker, which
asynchronously calculates the reputation rating.

The reputation rating is calculated based on the hash as key information.
In real-world systems, additional behavioral data would also be considered
to perform the analysis.

Currently, the analyzer is a simple mock that calculates a rating solely from the hash,
but in real-world systems, this would involve more sophisticated logic.

Results currently are stored in MemoryStorage, that can be replaced with
any persistent storage, so that subsequent requests return the already
calculated result without recalculation.


### Setup and run

1. Install dependencies:

    pip install -r requirements.txt

2. Run the server:

    python main.py

The service will be available at http://127.0.0.1:8000


### API Endpoints

"GET /getReputation/?hash_str=<hash>"
"GET /isReputationReady/request_id=<request_id>"

Responses json structure:
{
    "request_id": "uuid4 string",
    "hash_str": "hash string",
    "reputation": "UNKNOWN | LOW | MEDIUM | HIGH | CRITICAL",
    "status": "UNKNOWN | PENDING | SUCCEED | FAILED"
}

Statuses:

UNKNOWN - an unknown task
PENDING - the task in the queue
SUCCEED - the reputation is calculates successfully
FAILED - the reputation calculation was failed

Reputation levels:

UNKNOWN - the request_id/hash is unknown or the reputation is not calculated yet
LOW - the low reputation risk
MEDIUM - the medium reputation risk
HIGH - the high reputation risk
CRITICAL - the critical reputation risk

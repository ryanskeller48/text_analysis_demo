# Text Analysis Service

A simple Django Rest Framework API for evaluating different properties of text.  Contains 3 default analysis services (other services can be added):

- **Word Count**: Return the number of words in a text sample.

- **Sentiment Analysis**: Determine the mood of a text sample (e.g. happy, concerned, etc.).

- **Entity Recognition**: Identify "named entities" (e.g. people, organizations, etc.).

-------------------------

### Prerequisites

- Python 3
- pip
- A Linux-like environment to run the scripts

It is recommended to run this app in a virtual environment, e.g.
```
virtualenv text_analysis
source text_analysis/bin/activate
```

-------------------------

### Running the tests

*(From the root of the project)*

```
./run_tests.sh
```

-------------------------

## Running the server

*(From the root of the project)*

```
./run_server.sh
```

Navigate to http://127.0.0.1:8000/ in your browser to interact with the Text Analysis API

--------------------------
### Sample operations


***Poll a service***

Request
```
HTTP POST /
{
    "service": "sentiment-analysis",
    "text": "Lorem ipsum dolor sit amet"
}
```
Response
```
HTTP 200 OK
{"result": "Happy"}
```

--------------

***Add a service***

Request
```
HTTP POST /add
{
    "name": "example-service",
    "url": "https://example.com"
}
```
Response
```
HTTP 201 Created
{"message": "Service registered successfully"}
```

---------------------

***Delete a service***

Request
```
HTTP POST /delete
{
    "name": "word-count",
}
```
Response
```
HTTP 200 OK
{"message": "Service word-count deleted successfully."}
```



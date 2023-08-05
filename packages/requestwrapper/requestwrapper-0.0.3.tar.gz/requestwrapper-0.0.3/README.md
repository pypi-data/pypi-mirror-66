# requestwrapper
A simple wrapper for the Python requests package

## Motivation
Common use cases when dealing with requests are: 
* handling response errors
* repeating a request until succesfull response
* executing multiple requests
* saving response (html, pdf) to disk

Requestwrapper implements simple methods to perform such tasks without having to write your own code.

## Features
* Parameterize HTTP method using the method-argument
* Handle HTTP errors (status_code>299) by returning the raw response instead of json
* Retry failed requests n-times
* Print request-response to console
* Save response content to disk

## Prerequisites
1. the requests module (https://pypi.org/project/requests/)

## Installing
Hosted on PyPI: (https://pypi.org/project/requestwrapper/) With pip: pip install requestwrapper

## Usage
```
import requestwrapper.Request
#initialize the Request object
Request0=requestwrapper.Request.Request()

# workhorse function: send_request
res=Request0.send_request(url='https://nu.nl',method='GET')

# save response content to disk
Request0.save_response('nu.txt')

```

## Examples
TODO

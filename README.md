# Echo http requests

This simple GoogleAppEngine app can be used to test http requests expected on a predefined url when you don't have a publicly available IP address. It is available on http://echo-http-requests.appspot.com .

Just use a url like:

    http://echo-http-requests.appspot.com/push/YOUR_RANDOM_STRING_HERE

Then retrieve requests received on that url with:

    http://echo-http-requests.appspot.com/pull/THE_SAME_RANDOM_STRING_HERE

Requests can be retrieved only once and requests older than 15 minutes will be removed.

[The source is here](http://github.com/tkrajina/echo-http-requests).

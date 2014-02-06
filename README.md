# Echo http requests

This GoogleAppEngine app can be used to test http requests expected on a predefined url when you don't have a publicly available IP address. It is available on http://echo-http-requests.appspot.com .

Just use a url like:

    http://echo-http-requests.appspot.com/push/YOUR_RANDOM_STRING_HERE

Then retrieve requests received on that url with:

    http://echo-http-requests.appspot.com/pull/YOUR_RANDOM_STRING_HERE

Requests can be retrieved only once and requests older than 15 minutes will be removed.

If you need just informations about your own request (IP address, user agent, all headers) it can be retrieved with:

    http://echo-http-requests.appspot.com/echo

[Source](http://github.com/tkrajina/echo-http-requests).

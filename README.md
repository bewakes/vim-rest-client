# vim-rest-client

A HTTP client for vim.  

Kind of an alternative to Postman and similar GUI applications.

## Usage
Currently, the following is a sample request
```yaml
GET http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en

Accept: application/json
Authorization: Token UO49U3OIWWIWEUFOWIRJFL

```
To get response, run command in normal mode `RunVrc`, and the result is in a vertical splitted buffer. 

I know, this is very primitive and only currently works for `GET` request. But I'll be adding features very soon.

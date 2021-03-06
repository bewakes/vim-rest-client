# vim-rest-client

A HTTP client for vim.  

Kind of an alternative to Postman and similar GUI applications.

## Installation
It's very easy. Install [Plug](https://github.com/junegunn/vim-plug). And in your `vimrc` file, within `Plug` block, add `"bewakes/vim-rest-client"`. Reload vim and then run `:PlugInstall`.

## Usage

Sample request
```yaml
GET http://api.forismatic.com/api/1.0/? 

Accept: application/json
Authorization: Token UO49U3OIWWIWEUFOWIRJFL


method=getQuote
format=json
lang=en

```
Note that, the first line is the method and uri.  

If headers are present, separate them with a blank line from method.  

And if body is present, separate the body with two blank lines.  

Another request sample.
```yaml
PUT http://testing-vrc.com

Authorization: Token sometoken
Content-Type: application/json
Accept: application/json


{
 "a": 1,
 "what": "nothing"
}
```

To get response, run command `:RunVrc`, and the result appears in a vertical splitted buffer. 

**NOTE**: Multiple requests can be present in a single file. The request block where the cursor lies will be executed.

## Authorization
Currently only **Basic authorization is supported**. To have basic authorization, in the `Authorization` header field, provide value as `$BASIC(username, password)`. For example:
```yaml
PUT http://testing-vrc.com

Authorization: $BASIC(user, password)
Content-Type: application/json
Accept: application/json
```

## Syntax Highlighting
For syntax highlighting, either save the request file with `.vrc` extension or run command `:set ft=vrc`

## TODO
- Make this async
- Add more features
- Make configurable

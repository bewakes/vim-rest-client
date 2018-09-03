# vim-rest-client

A HTTP client for vim.  

Kind of an alternative to Postman and similar GUI applications.

## Usage
Currently, the following is a sample request
```
<request>
    <header>
        Authorization: Token bibek
    </header>

    <method>
        GET https://bewakes.com/til/api/?random=1
    </method>

    <body>
        a=1
        b=2
        c=3
    </body>
</request>
```
Note that, the format is similar to html. The root tag is `<request>`.  

To get response, run command in normal mode `:call RestClient()`, and the result is in a vertical splitted buffer. 

I know, this is very primitive and only currently works for `GET` request. But I'll be adding features very soon.

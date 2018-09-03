# vim-rest-client

A HTTP client for vim.  

Kind of an alternative to Postman and similar GUI applications.

## Usage
Currently, the following is a sample request
```
#############
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
#############
```
Note that, the format is similar to html. And request is inside two lines containing `###`.  

To get response, run command in normal mode `:call RestClient()`, and the result is in a vertical splitted buffer. 

I know, this is very primitive and only currently works for `GET` request. But I'll be adding features very soon.

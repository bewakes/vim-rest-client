if exists('b:current_syntax')
    finish
endif

syntax keyword httpMethod GET PUT POST DELETE OPTIONS HEAD get put post delete options head PATCH patch
syntax keyword httpHeaderKey Accept Authorization Content-Type Connection Length User-Agent Location Cookie
syntax match uri /http.*/
highlight link httpMethod Keyword
highlight link httpHeaderKey Exception
highlight link uri String

let b:current_syntax = 'vrc'

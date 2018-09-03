let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import rest 
EOF

function! ProcessClientOutput(output)
    let l:result = "========\nRESPONSE\n========\n\n"
    let l:result = l:result.a:output['method']." ".a:output['url']."  ".a:output['status_code']."\n\n"

    " Calculate headers
    let l:headers = []
    for [k, v] in items(a:output['headers'])
        call add(l:headers, k.": ".v)
    endfor
    " Append headers
    let l:result = l:result."HEADER\n======\n".join(l:headers, "\n")."\n\n"
    " Append body
    let l:result = l:result."BODY\n====\n".join(a:output['body'], "\n")
    return l:result
endfunction

function! RunClient()
    " Get current line number
    let l:line_num=line(".")
    " Get all text
    let l:all_text=join(getline(1,'$'), "\n")

    " Call our mighty python function, this will set a dict to
    " l:vim_rest_client_data
    python3 rest.process_and_call(vim.eval('l:line_num'), vim.eval('l:all_text'))

    " Output variable whose content is dumped to buffer
    let l:output = ""

    " Process the output dict, first check for error
    if l:vim_rest_client_data['error']
        let l:output = l:output."ERROR\n=====\n\n".vim_rest_client_data['message']
    else
        let l:output = ProcessClientOutput(vim_rest_client_data)
    endif
    vne | put = l:output
    normal !gg
    set noma
endfunction

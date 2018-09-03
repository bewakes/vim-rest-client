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
    let l:result = l:result."BODY\n====\n".a:output['body']
    return l:result
endfunction

function! RunClient()
    " Get current line number
    let l:line_num=line(".")
    " Get all text
    let l:all_text=join(getline(1,'$'), "\n")

    " Call our mighty python function which will write result to file and 
    " store path in variable vrc_result_path
    python3 rest.process_and_call(vim.eval('l:line_num'), vim.eval('l:all_text'))

    echo vrc_result_path
    vne | execute "0read " . vrc_result_path
    normal !gg
    set noma
endfunction

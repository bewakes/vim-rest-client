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

function! RunClient()
    " Get current line number
    let l:line_num=line(".")
    " Get all text
    let l:all_text=join(getline(1,'$'), "\n")

    " Call our mighty python function which will write result to file and 
    " store path in variable vrc_result_path
    python3 rest.process_and_call(vim.eval('l:line_num'), vim.eval('l:all_text'))

    " If buffer exist, remove it and then only create new
    bufdo if @% == "vrc_resp" | set ma | endif
    try
        bd! vrc_resp
    catch
    endtry

    " TODO: bug when buffer is deleted and again client run
    vne vrc_resp | execute "0read " . vrc_result_path
    set wrap
    normal !gg
    set noma
endfunction

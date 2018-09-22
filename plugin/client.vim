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
    " clear vrc_result_path file
    " Get current line number
    let l:line_num=line(".")
    " Get all text
    let l:all_text=join(getline(1,'$'), "\n")

    " Call our mighty python function which will write result to file and 
    " store path in variable vrc_result_path
    let l:output_path="/tmp/vrc_resp"
    silent execute "!echo '' >" l:output_path
    python3 rest.process_and_call(vim.eval('l:line_num'), vim.eval('l:all_text'), vim.eval('l:output_path'))

    " If buffer exists, remove it and then only create new
    bufdo if @% == "vrc_resp" | set ma | endif
    bufdo if @% == "vrc_resp" | bd! | endif


    vne | execute "0read " . l:output_path
    execute "file vrc_resp"
    setlocal buftype=nofile
    set ft=vrc
    set wrap
    normal !gg
    set noma
endfunction


" Setting file type
au BufNewFile,BufRead *.vrc set filetype=vrc

command! -nargs=0 RunVrc call RunClient()

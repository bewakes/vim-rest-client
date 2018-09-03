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

function! Process()
    let l:line_num=line(".")
    let l:all_text=join(getline(1,'$'), "\n")
    python3 rest.process_and_call(vim.eval('l:line_num'), vim.eval('l:all_text'))
    echo vim_rest_client_data
    echo "woo ho""
endfunction

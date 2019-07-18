"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugins
"""""""""""""""""""""""""""""""""""""""""""""""""

call plug#begin()

Plug 'easymotion/vim-easymotion'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-fugitive'
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'w0rp/ale'
Plug 'chiel92/vim-autoformat'

"" fuzzy finder
Plug 'junegunn/fzf', { 'do': './install --bin' }

"" Autocomplete
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
Plug 'zchee/deoplete-clang'

"" color
Plug 'nanotech/jellybeans.vim'

call plug#end()


" pure vim

set autoread
set swapfile
set tildeop
set ttyfast
set visualbell
set wildmenu
set wildmode=full

"" space setting

set autoindent
set list
set shiftround
set shiftwidth=2
set smartindent
set smarttab
set tabstop=2

"" appearance

syntax on
set backspace=indent,eol,start
set colorcolumn=80
set completeopt=menu
set cursorline
set hlsearch
set inccommand=nosplit
set incsearch
set number
set relativenumber
set shortmess=a
set showcmd
set showmatch
set showmode
set splitbelow
set splitright
set wrap

"""""""""""""""""""""""""""""""""""""""""""""""""
"" keymaps
"""""""""""""""""""""""""""""""""""""""""""""""""
let mapleader="C-<"


"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugin settings
"""""""""""""""""""""""""""""""""""""""""""""""""

" deoplete
let g:deoplete#enable_at_startup=1

" fzf
nnoremap <leader>b :Buffers<cr>
nnoremap <leader>c :History:<cr>
nnoremap <leader>f :Files<cr>
nnoremap <leader>g :GFiles<cr>
nnoremap <leader>h :History<cr>
nnoremap <leader>l :Lines<cr>
nnoremap <leader>m :Maps<cr>
nnoremap <leader>r :Ag<cr>

"""""""""""""""""""""""""""""""""""""""""""""""""
"" Automation
"""""""""""""""""""""""""""""""""""""""""""""""""
" Auto commands
autocmd VimEnter * PlugUpgrade
autocmd VimEnter * PlugInstall
autocmd VimEnter * PlugUpdate
autocmd TermResponse * colorscheme jellybeans
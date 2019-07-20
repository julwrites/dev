"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugins
"""""""""""""""""""""""""""""""""""""""""""""""""

call plug#begin()

"" Navigation
Plug 'scrooloose/nerdtree'
Plug 'easymotion/vim-easymotion'
Plug 'tpope/vim-surround'
Plug 'wellle/targets.vim'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'rhysd/clever-f.vim'
Plug 'nelstrom/vim-visual-star-search'
Plug 'ntpeters/vim-better-whitespace'

"" Language Support
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'tpope/vim-commentary'

"" Formatting
Plug 'tommcdo/vim-lion'
Plug 'chiel92/vim-autoformat'

"" Themes
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'nanotech/jellybeans.vim'

call plug#end()


"""""""""""""""""""""""""""""""""""""""""""""""""
"" vim settings
"""""""""""""""""""""""""""""""""""""""""""""""""

syntax on

" Files
set autoread
set confirm

" Key Operations
set tildeop

set backspace=indent,eol,start

" Terminal
set ttyfast

set splitbelow
set splitright

set lazyredraw

set guioptions=
set guifont=FiraCode:h14
set termguicolors

" Status Bar
set visualbell

set wildmenu
set wildmode=full

set completeopt=menu

set inccommand=nosplit

set showcmd
set showmatch
set showmode

" Formatting
set autoindent

set smarttab
set expandtab
set tabstop=2

set ignorecase
set smartcase
set infercase

set synmaxcol=120

" Search
set hlsearch
set incsearch

" Markers
set cursorline
set ruler

set nowrap
set number
set relativenumber

" System
set clipboard=unnamed

"""""""""""""""""""""""""""""""""""""""""""""""""
"" keymaps
"""""""""""""""""""""""""""""""""""""""""""""""""

let mapleader="<C-<>"

" Remap terminal escape to esc key
:tnoremap <Esc><Esc> <C-\><C-n>

"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugin settings
"""""""""""""""""""""""""""""""""""""""""""""""""
" NERDTree
map <C-n> :NERDTreeToggle<CR>

" CtrlP
map <C-p> :CtrlP<CR>

" CoC
let g:coc_global_extensions=['coc-ccls', 'coc-python', 'coc-tsserver', 'coc-rls', 'coc-vetur', 'coc-json']
inoremap <silent><expr> <tab><tab> coc#refresh()
map <M-s> :CocConfig<CR>

" Autoformat
let g:autoformat_autoindent = 0
let g:autoformat_retab = 0
let g:autoformat_remove_trailing_spaces = 0

"""""""""""""""""""""""""""""""""""""""""""""""""
"" Automation
"""""""""""""""""""""""""""""""""""""""""""""""""
" Auto commands
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * PlugUpgrade
autocmd VimEnter * PlugInstall
autocmd VimEnter * PlugUpdate
autocmd VimEnter * UpdateRemotePlugins
autocmd VimEnter * AirlineTheme solarized
autocmd VimEnter * colorscheme jellybeans
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | exe 'cd '.argv()[0] | endif
autocmd VimEnter * redraw!

" File commands
autocmd BufWrite * Autoformat
autocmd FileType vim,tex let b:autoformat_autoindent=0
autocmd BufNewFile,BufRead Jenkinsfile setf groovy

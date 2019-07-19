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
Plug 'chiel92/vim-autoformat'
Plug 'tpope/vim-commentary'

"" Autocomplete
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
Plug 'zchee/deoplete-clang'
Plug 'tommcdo/vim-lion'

"" Themes
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'nanotech/jellybeans.vim'

call plug#end()


"""""""""""""""""""""""""""""""""""""""""""""""""
"" vim settings
"""""""""""""""""""""""""""""""""""""""""""""""""

syntax on

set autoread
set confirm

set tildeop

set ttyfast

set visualbell

set wildmenu
set wildmode=full

set autoindent

set smarttab
set expandtab
set tabstop=2

set ignorecase
set smartcase
set infercase

set backspace=indent,eol,start

set synmaxcol=200

set ruler

set completeopt=menu

set cursorline

set hlsearch
set incsearch

set inccommand=nosplit

set nowrap
set number
set relativenumber

set showcmd
set showmatch
set showmode

set splitbelow
set splitright

set lazyredraw

" colors
set guioptions=
set guifont=FiraCode:h14
set termguicolors

set clipboard=unnamed

"""""""""""""""""""""""""""""""""""""""""""""""""
"" keymaps
"""""""""""""""""""""""""""""""""""""""""""""""""

let mapleader="<"

" Remap terminal escape to esc key
:tnoremap <Esc><Esc> <C-\><C-n>

"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugin settings
"""""""""""""""""""""""""""""""""""""""""""""""""
" NERDTree
map <C-n> :NERDTreeToggle<CR>

" CtrlP
map <C-p> :CtrlP<CR>

" deoplete
let g:deoplete#enable_at_startup=1

" coc
inoremap <silent><expr> <tab> coc#refresh()
map <M-s> :CocConfig<CR>

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
autocmd BufWrite * Autoformat

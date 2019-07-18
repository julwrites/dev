"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugins
"""""""""""""""""""""""""""""""""""""""""""""""""

call plug#begin()

"" Navigation
Plug 'scrooloose/nerdtree'
Plug 'easymotion/vim-easymotion'
Plug 'tpope/vim-surround'
Plug 'ctrlpvim/ctrlp.vim'

"" Language Support
Plug 'w0rp/ale'
Plug 'chiel92/vim-autoformat'

"" Autocomplete
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
Plug 'zchee/deoplete-clang'

"" Themes
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'nanotech/jellybeans.vim'
Plug 'KKPMW/sacredforest-vim'

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
let mapleader="<"

" Remap terminal escape to esc key
:tnoremap <Esc><Esc> <C-\><C-n>

" Remap ctrl p to ctrl ,
let g:ctrlp_map = '<C-,>'
let g:ctrlp_cmd = 'CtrlP'

"""""""""""""""""""""""""""""""""""""""""""""""""
"" plugin settings
"""""""""""""""""""""""""""""""""""""""""""""""""
" NERDTree
map <C-n> :NERDTreeToggle<CR>

" deoplete
let g:deoplete#enable_at_startup=1

" colorschemes
set guifont=FiraCode:h14 noanti
set termguicolors

"""""""""""""""""""""""""""""""""""""""""""""""""
"" Automation
"""""""""""""""""""""""""""""""""""""""""""""""""
" Auto commands
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * PlugUpgrade
autocmd VimEnter * PlugInstall
autocmd VimEnter * PlugUpdate
autocmd VimEnter * UpdateRemotePlugins
autocmd VimEnter * colorscheme sacredforest
autocmd VimEnter * AirlineTheme solarized
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | exe 'cd '.argv()[0] | endif

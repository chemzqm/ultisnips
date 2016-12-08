let s:save_cpo = &cpo
set cpo&vim

let s:source = {
      \ 'name': 'ultisnips',
      \ 'hooks': {},
      \ 'description' : 'manage ultisnips',
      \ 'syntax' : 'uniteSource__Ultisnips',
      \ 'action_table': {},
      \ 'default_action': 'expand',
      \ }

let s:source.action_table.edit = {
            \ 'description' : 'edit snippet file',
            \ 'is_quit' : 1
            \ }

let s:source.action_table.expand = {
      \ 'description': 'expand the current snippet',
      \ 'is_quit': 1
      \}

function! s:source.hooks.on_syntax(args, context) abort
  syntax case ignore
  syntax match uniteSource__UltisnipsHeader /^.*$/
        \ containedin=uniteSource__Ultisnips
  syntax match uniteSource__UltisnipsPath /\v^\s.{-}\ze\s/ contained
        \ containedin=uniteSource__UltisnipsHeader
  syntax match uniteSource__UltisnipsTrigger /\%14c.*\%38c/ contained
        \ containedin=uniteSource__UltisnipsHeader
  syntax match uniteSource__UltisnipsDescription /\%39c.*$/ contained
        \ containedin=uniteSource__UltisnipsHeader
  highlight default link uniteSource__UltisnipsPath Comment
  highlight default link uniteSource__UltisnipsTrigger Identifier
  highlight default link uniteSource__UltisnipsDescription Statement
endfunction

function! s:source.action_table.edit.func(candidate)
  let path = a:candidate.action__path
  let line = a:candidate.action__line
  exe 'edit ' . path
  exe 'normal! ' . line . 'Gzz'
endfunction

function! s:source.action_table.expand.func(candidate)
  let delCurrWord = (getline(".")[col(".")-1] ==# " ") ? "" : "diw"
  exe "normal " . delCurrWord . "a" . a:candidate['source__trigger'] . " "
  call UltiSnips#ExpandSnippet()
  return ''
endfunction


function! s:source.gather_candidates(args, context)
  let default_val = {'word': '', 'unite__abbr': '', 'is_dummy': 0, 'source':
        \  'ultisnips', 'unite__is_marked': 0, 'kind': 'jump_list', 'is_matched': 1,
        \    'is_multiline': 0, 'action__col': 0}
  if get(a:args, 0, '') ==# 'all'
    let snippet_list = UltiSnips#SnippetsInCurrentScope(1)
  else
    let snippet_list = UltiSnips#SnippetsInCurrentScope(0)
  endif
  let canditates = []
  for item in snippet_list
    let curr_val = copy(default_val)
    let list = split(item.location, ':')
    let curr_val['action__path'] = list[0]
    let file = fnamemodify(list[0], ':t:r')
    let curr_val['action__line'] = list[1]
    let curr_val['word'] = item.key. " " . item.description
    let curr_val['abbr'] = printf('%-*s', 12, file) . printf('%-*s', 20, item.key) . "     " . item.description
    let curr_val['source__trigger'] = item.key
    call add(canditates, curr_val)
  endfor

  return canditates
endfunction

function! s:Pad(str)
  let emptystr = "                 "
  let pad = substitute(emptystr, '\v\s{' . len(a:str) . '}', '', '')
  return a:str . pad
endfunction

function! unite#sources#ultisnips#define()
  return s:source
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

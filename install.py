#!/usr/bin/env python
import os
import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def install(dotfile, destination):
    source = os.path.join(BASE_DIR, dotfile)
    destination = os.path.expanduser(destination)

    print "installing %s -> %s..." % (source, destination)
    if os.path.lexists(destination):
        os.remove(destination)

    os.symlink(source, destination)

dotfiles = [('git/cvsignore', '~/.cvsignore'),
            ('git/git_template', '~/.git_template'),
            ('git/gitconfig', '~/.gitconfig'),
            ('git/gitk', '~/.gitk'),

            ('vim/vim', '~/.vim'),
            ('vim/vimrc', '~/.vimrc'),

            ('oh-my-zsh', '~/.oh-my-zsh'),
            ('oh-my-zsh/zshrc', '~/.zshrc'),
           ]

for dotfile, destination in dotfiles:
    install(dotfile, destination)

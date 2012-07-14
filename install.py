#!/usr/bin/env python
import os
import platform
import shutil
import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def install(dotfile, destination):
    source = os.path.join(BASE_DIR, dotfile)
    destination = os.path.expanduser(destination)

    print "installing %s -> %s..." % (source, destination)
    if os.path.lexists(destination):
        if not os.path.islink(destination):
            while True:
                delete = raw_input("%s (%s) exists and isn't a symlink, delete? (Y/n) " % \
                                     (destination,
                                      'directory' if os.path.isdir(destination) else 'file'))
                delete = delete.strip().lower()
                if delete == 'y' or not delete:
                    delete = True
                    break
                elif delete == 'n':
                    delete = False
                    break
        else:
            delete = True

        if not delete:
            return

        if os.path.islink(destination) or \
           os.path.isfile(destination):
            os.remove(destination)
        else:
            shutil.rmtree(destination)

    os.symlink(source, destination)

dotfiles = [('git/cvsignore', '~/.cvsignore'),
            ('git/git_template', '~/.git_template'),
            ('git/gitconfig', '~/.gitconfig'),
            ('git/gitk', '~/.gitk'),

            ('vim/vim', '~/.vim'),
            ('vim/vimrc', '~/.vimrc'),

            ('oh-my-zsh', '~/.oh-my-zsh'),
            ('oh-my-zsh/zshrc', '~/.zshrc'),

            ('xmonad/xmonad', '~/.xmonad', 'linux'),
            ('xmonad/xmobarrc', '~/.xmobarrc', 'linux'),
           ]

for mapping in dotfiles:
    if len(mapping) == 3:
        source, destination, system = mapping
    else:
        source, destination = mapping
        system = None

    if system and not platform.system().lower() == system:
        continue

    install(source, destination)

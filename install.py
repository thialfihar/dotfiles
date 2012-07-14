#!/usr/bin/env python
import os
import platform
import shutil
import subprocess

class Dotfile:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, source, destination, platform=None, test=None):
        self.source = source
        self.destination = destination
        self.platform = platform
        self.test = test

    def install(self):
        if self.platform:
            if self.platform != platform.system().lower():
                print "ignoring %s because it requires %s..." % (self.destination, self.platform)
                return

        if self.test:
            if subprocess.call(self.test, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE):
                print "ignoring %s because this test failed: %s" % (self.destination, self.test)
                return

        source = os.path.join(self.BASE_DIR, self.source)
        destination = os.path.expanduser(self.destination)

        print "installing %s -> %s..." % (self.source, self.destination)
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

dotfiles = [Dotfile('git/cvsignore', '~/.cvsignore'),
            Dotfile('git/git_template', '~/.git_template'),
            Dotfile('git/gitconfig', '~/.gitconfig'),
            Dotfile('git/gitk', '~/.gitk'),

            Dotfile('vim/vim', '~/.vim'),
            Dotfile('vim/vimrc', '~/.vimrc'),

            Dotfile('oh-my-zsh', '~/.oh-my-zsh'),
            Dotfile('oh-my-zsh/zshrc', '~/.zshrc'),

            Dotfile('xmonad/xmonad', '~/.xmonad', test="which xmonad"),
            Dotfile('xmonad/xmobarrc', '~/.xmobarrc', test="which xmobar"),
           ]

for dotfile in dotfiles:
    dotfile.install()

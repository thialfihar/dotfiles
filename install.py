#!/usr/bin/env python
import os
import platform
import shutil
import stat
import subprocess
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Base(object):
    def __init__(self, name=None, platform=None, test=None):
        self.name = name
        self.platform = platform
        self.test_command = test

    def test(self):
        if self.platform:
            if self.platform != platform.system().lower():
                print "ignoring %s because it requires %s..." % (self.name, self.platform)

        if self.test_command and \
           subprocess.call(self.test_command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            print "ignoring %s because this test failed: %s" % (self.name, self.test_command)
            return False

        return True

class Dotfile(Base):
    def __init__(self, source, destination, *args, **kwargs):
        super(Dotfile, self).__init__(*args, name=destination, **kwargs)
        self.source = source
        self.destination = destination

    def install(self):
        if not self.test():
            return

        source = os.path.join(BASE_DIR, self.source)
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

class Dotcommand(Base):
    def __init__(self, command, *args, **kwargs):
        super(Dotcommand, self).__init__(command, *args, **kwargs)
        self.command = command

    def execute(self):
        if not self.test():
            return

        tmp_filename = '/tmp/dotfiles_install_command'
        print "executing: %s" % self.command
        f = file(tmp_filename, 'w')
        f.write("#!/bin/bash -e\ncd '%s'\n" % BASE_DIR)
        f.write(self.command)
        f.close()
        os.chmod(tmp_filename, stat.S_IRWXU)
        if subprocess.call(tmp_filename, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE):
             print "something went wrong there"
             sys.exit(-1)

        os.remove(tmp_filename)


dotfiles = [Dotfile('git/cvsignore', '~/.cvsignore'),
            Dotfile('git/git_template', '~/.git_template'),
            Dotfile('git/gitconfig', '~/.gitconfig'),
            Dotfile('git/gitk', '~/.gitk'),

            Dotfile('vim/vim', '~/.vim'),
            Dotfile('vim/vimrc', '~/.vimrc'),

            Dotfile('oh-my-zsh', '~/.oh-my-zsh'),
            Dotfile('oh-my-zsh/zshrc', '~/.zshrc'),

            Dotfile('Xmodmap', '~/.Xmodmap', platform="linux"),
            Dotfile('xmonad/xmonad', '~/.xmonad', test="which xmonad"),
            Dotfile('xmonad/xmobarrc', '~/.xmobarrc', test="which xmobar"),
            Dotfile('i3/i3', '~/.i3', test="which i3"),
            Dotfile('bin/battery.py', '~/bin/battery.py', test="which xmobar"),
            Dotfile('modules/ls-colors-solarized/dircolors', '~/.dircolors'),
            Dotfile('gtkrc-2.0', '~/.gtkrc-2.0'),
           ]

scripts = ['start_cmus_in_tmux.sh', 'suspend_laptop', 'themeless', 'firefox',
    'libreoffice', 'set_volume', 'get_volume', 'set_brightness',
    'set_keyboard_brightness', 'myi3status.py']
for script in scripts:
    dotfiles.append(Dotfile('bin/' + script, '~/bin/' + script))


commands = []

for dotfile in dotfiles:
    dotfile.install()

for command in commands:
    command.execute()


#!/usr/bin/env python3
import os
import platform
import shutil
import stat
import subprocess
import sys
from glob import glob

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Base(object):
    def __init__(self, name=None, platform=None, test=None):
        self.name = name
        self.platform = platform
        self.test_command = test

    def test(self):
        if self.platform:
            if self.platform != platform.system().lower():
                print("ignoring %s because it requires %s..." % (self.name, self.platform))

        if self.test_command and \
           subprocess.call(self.test_command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            print("ignoring %s because this test failed: %s" % (self.name, self.test_command))
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

        print("installing %s -> %s..." % (self.source, self.destination))
        directory = os.path.dirname(destination)
        if not os.path.exists(directory):
            print("creating directory %s..." % directory)
            os.makedirs(directory)

        if os.path.lexists(destination):
            if not os.path.islink(destination):
                while True:
                    replace = input("%s (%s) exists and isn't a symlink, backup and replace it? (Y/n) " %
                                    (destination, 'directory' if os.path.isdir(destination) else 'file'))
                    replace = replace.strip().lower()
                    if replace == 'y' or not replace:
                        replace = True
                        backup = True
                        break
                    elif replace == 'n':
                        replace = False
                        break
            else:
                replace = True
                backup = False

            if not replace:
                return

            if backup:
                i = 0
                backup_name = destination.rstrip('/') + '.backup.%s' % i
                while os.path.lexists(backup_name):
                    i += 1
                    backup_name = destination.rstrip('/') + '.backup.%s' % i

                shutil.move(destination, backup_name)

            else:
                if os.path.islink(destination) or os.path.isfile(destination):
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
        print("executing: %s" % self.command)
        f = open(tmp_filename, 'w')
        f.write("#!/bin/bash -e\ncd '%s'\n" % BASE_DIR)
        f.write(self.command)
        f.close()
        os.chmod(tmp_filename, stat.S_IRWXU)
        if subprocess.call(tmp_filename, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            print("something went wrong there")
            sys.exit(-1)

        os.remove(tmp_filename)


dotfiles = [Dotfile('git/cvsignore', '~/.cvsignore'),
            Dotfile('git/git_template', '~/.git_template'),
            Dotfile('git/gitconfig', '~/.gitconfig'),
            Dotfile('git/gitk', '~/.gitk'),
            Dotfile('git/gitignore_global', '~/.gitignore_global'),

            Dotfile('spacemacs/spacemacs', '~/.spacemacs'),
            Dotfile('spacemacs/layers', '~/.emacs.d/private/layers'),

            Dotfile('vim/vim', '~/.vim'),
            Dotfile('vim/vimrc', '~/.vimrc'),

            Dotfile('vimperator/vimperator/colors', '~/.vimperator/colors'),
            Dotfile('vimperator/vimperatorrc', '~/.vimperatorrc'),

            Dotfile('oh-my-zsh', '~/.oh-my-zsh'),
            Dotfile('oh-my-zsh/zshrc', '~/.zshrc'),
            Dotfile('oh-my-zsh/zshenv.osx', '~/.zshenv', platform='darwin'),

            Dotfile('terminator', '~/.config/terminator'),
            Dotfile('roxterm/Global', '~/.config/roxterm.sourceforge.net/Global'),
            Dotfile('roxterm/Colours', '~/.config/roxterm.sourceforge.net/Colours'),
            Dotfile('roxterm/Profiles', '~/.config/roxterm.sourceforge.net/Profiles'),

            Dotfile('Xmodmap', '~/.Xmodmap', platform="linux"),
            Dotfile('i3/i3', '~/.i3', test="which i3"),
            Dotfile('i3/i3/i3blocks.conf', '~/.i3blocks.conf', test="which i3"),
            Dotfile('bin/battery.py', '~/bin/battery.py', test="which xmobar"),
            Dotfile('modules/ls-colors-solarized/dircolors', '~/.dircolors'),
            Dotfile('gtkrc-2.0', '~/.gtkrc-2.0'),
            Dotfile('system/compton.conf', '~/.config/compton.conf'),
            Dotfile('modules/docker-zsh-completion/_docker', '~/.zsh/completion/_docker'),

            Dotfile('hermod/lib/offlineimap.py', '~/.offlineimap.py'),
            Dotfile('hermod/lib/hermod', '~/.emacs.d/private/hermod'),
            ]

for script in glob("bin/*") + glob("hermod/bin/*"):
    dotfiles.append(Dotfile(script, os.path.join("~/bin", os.path.basename(script))))

commands = []

for dotfile in dotfiles:
    dotfile.install()

for command in commands:
    command.execute()

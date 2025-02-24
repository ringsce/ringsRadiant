# -*- mode: python -*-
# GtkRadiant build scripts
# TTimo <ttimo@ttimo.net>
# http://scons.org/

import sys, os, platform, pickle
import utils, config

# Determine platform and architecture
current_platform = platform.system()
machine_arch = os.uname().machine if hasattr(os, 'uname') else ''

# Optionally, set extra flags based on platform/architecture
extra_platforms = []
if current_platform == 'Darwin' and machine_arch in ['arm64', 'arm64e']:
    print("Detected macOS Silicon (ARM64)")
    extra_platforms.append('macos-m1')
elif current_platform == 'Linux' and machine_arch in ['aarch64', 'arm64']:
    print("Detected Linux ARM64")
    extra_platforms.append('linux-arm64')
elif current_platform == 'Windows':
    # For Windows, you might have separate logic for x86_64 or ARM64:
    if machine_arch.lower().startswith('arm'):
        extra_platforms.append('windows-arm64')
    else:
        extra_platforms.append('windows-x86_64')

conf_filename = 'site.sconf'

try:
    sys.argv.index('-h')
except Exception:
    pass
else:
    Help(
"""
======================================================================
GtkRadiant build system quick help

You need scons v0.97.0d20070918.r2446 or newer

Default build (release), just run scons at the toplevel

debug build:
$ scons config=debug

build using 8 parallel build jobs
but do not download any game packs
$ scons -j8 --no-packs
======================================================================
""")
    Return()

AddOption('--no-packs',
    dest='no_packs',
    action='store_true',
    help="don't fetch game packs")

# Add a command-line option for useGtk
AddOption('--use-gtk',
    dest='useGtk',
    action='store_true',
    default=False,
    help="Enable GTK support")

# Retrieve the option value (SCons global variable)
useGtk = GetOption('useGtk')

active_configs = []

# load up configurations from the save file
if os.path.exists(conf_filename):
    f = open(conf_filename, 'rb')
    print('reading saved configuration from site.conf')
    try:
        while True:
            c = pickle.load(f)
            active_configs.append(c)
    except EOFError:
        pass
    f.close()

# read the command line and build configs
config_statements = sys.argv[1:]
active_configs = config.ConfigParser().parseStatements(active_configs, config_statements)
assert(len(active_configs) >= 1)

# Optionally, append extra platform info to each configuration
for c in active_configs:
    if hasattr(c, 'platforms'):
        for plat in extra_platforms:
            if plat not in c.platforms:
                c.platforms.append(plat)
    else:
        # If configuration doesn't already have a platforms list, create one.
        c.platforms = extra_platforms[:]

# save the config
print('saving updated configuration')
f = open(conf_filename, 'wb')
for c in active_configs:
    pickle.dump(c, f, -1)
f.close()

print('emit build rules')
for c in active_configs:
    print('emit configuration: %s' % repr(c))
    c.emit()

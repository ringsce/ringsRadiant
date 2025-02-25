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
        """
    )
    Return()

AddOption('--no-packs',
    dest='no_packs',
    action='store_true',
    help="don't fetch game packs")

AddOption('--use-gtk',
    dest='useGtk',
    action='store_true',
    default=False,
    help="Enable GTK support")

useGtk = GetOption('useGtk')

active_configs = []

if os.path.exists(conf_filename):
    with open(conf_filename, 'rb') as f:
        print('reading saved configuration from site.sconf')
        try:
            while True:
                c = pickle.load(f)
                active_configs.append(c)
        except EOFError:
            pass

config_statements = sys.argv[1:]
config_statements = sys.argv[1:]
active_configs = config.ConfigParser().parseStatements(active_configs, config_statements)
active_configs = config.ConfigParser().parseStatements(active_configs, config_statements)
assert len(active_configs) >= 1, "No active configurations found!"

# Append extra platform info to each configuration
for c in active_configs:
    if hasattr(c, 'platforms'):
        for plat in extra_platforms:
            if plat not in c.platforms:
                c.platforms.append(plat)
    else:
        c.platforms = extra_platforms[:]

# Save the updated configuration
print('saving updated configuration')
with open(conf_filename, 'wb') as f:
    for c in active_configs:
        pickle.dump(c, f, -1)

# Emit build rules using the configuration's emit() method.
print('emit build rules')
for c in active_configs:
    print('emit configuration: %s' % repr(c))
    c.emit()  # Call the emit() method on each configuration.

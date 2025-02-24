#!/usr/bin/env python3
# version and about message management
# NOTE: this module is meant to be used on all platforms, it is not SCons centric

import sys, re, os

def get_version():
    # version
    with open('include/version.default', 'r') as f:
        buffer = f.read()
    line = buffer.split('\n')[0]
    sys.stdout.write("version: %s\n" % line)
    exp = re.compile('^1\\.([^\\.]*)\\.([0-9]*)')
    (major, minor) = exp.findall(line)[0]
    sys.stdout.write("minor: %s major: %s\n" % (minor, major))
    return (line, major, minor)

def radiant_makeversion(append_about):
    (line, major, minor) = get_version()

    # Determine extra architecture-specific defines
    arch_define = ""
    current_platform = os.uname().sysname if hasattr(os, 'uname') else os.name
    machine_arch = os.uname().machine if hasattr(os, 'uname') else ""
    if current_platform == 'Darwin' and machine_arch in ['arm64', 'arm64e']:
        arch_define = '#define RADIANT_ARCH "macos-m1"\n'
        sys.stdout.write("Detected macOS Silicon (ARM64)\n")
    elif current_platform == 'Linux' and machine_arch in ['aarch64', 'arm64']:
        arch_define = '#define RADIANT_ARCH "linux-arm64"\n'
        sys.stdout.write("Detected Linux ARM64\n")
    else:
        arch_define = '#define RADIANT_ARCH "generic"\n'
        sys.stdout.write("Detected generic architecture\n")

    # Write version.h with optional architecture define
    with open('include/version.h', 'w') as f:
        f.write('// generated header, see makeversion.py\n')
        f.write('#define RADIANT_VERSION "%s"\n' % line)
        f.write('#define RADIANT_MINOR_VERSION "%s"\n' % minor)
        f.write('#define RADIANT_MAJOR_VERSION "%s"\n' % major)
        f.write(arch_define)

    with open('include/RADIANT_MINOR', 'w') as f:
        f.write(minor)

    with open('include/RADIANT_MAJOR', 'w') as f:
        f.write(major)

    with open('include/version', 'w') as f:
        f.write(line)

    # aboutmsg
    aboutfile = 'include/aboutmsg.default'
    if 'RADIANT_ABOUTMSG' in os.environ:
        aboutfile = os.environ['RADIANT_ABOUTMSG']
    sys.stdout.write("about message is in %s\n" % aboutfile)
    with open(aboutfile, 'r') as f:
        buffer = f.read()
    about_line = buffer.split('\n')[0]

    # optional additional message
    if append_about is not None:
        about_line += append_about
    sys.stdout.write("about: %s\n" % about_line)
    with open('include/aboutmsg.h', 'w') as f:
        f.write('// generated header, see makeversion.py\n')
        f.write('#define RADIANT_ABOUTMSG "%s"\n' % about_line)

# can be used as module (scons build), or by direct call
if __name__ == '__main__':
    radiant_makeversion(None)

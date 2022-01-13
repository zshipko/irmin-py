import cffi  # type: ignore
import os


def find_path(paths):
    for prefix in paths:
        if os.path.exists(os.path.join(
                prefix, "lib", "libirmin.so")) and os.path.exists(
                    os.path.join(prefix, "include", "irmin.h")):
            return prefix
    raise Exception(
        "Unable to detect libirmin path, try setting LIBIRMIN_PREFIX")


prefix = find_path([
    os.getenv("LIBIRMIN_PREFIX", ""),
    os.path.join(os.getenv("OPAM_SWITCH_PREFIX", "_opam"), "lib", "libirmin"),
    os.path.dirname(__file__),
    os.path.expanduser("~/.local"),
    "/usr/local",
])

ffi = cffi.FFI()
with open(os.path.join(prefix, "include", "irmin.h")) as h_file:
    lines = h_file.readlines()
    lines = [
        line for line in lines if '#include' not in line
        and '#define' not in line and 'static' not in line and '#' not in line
    ]
    lines.append("void free(void*);")
    ffi.cdef('\n'.join(lines))

lib = ffi.dlopen(os.path.join(prefix, "lib", "libirmin.so"))

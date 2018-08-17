# NewlibMarkup2SphinxConverter
This repo contains code for NewlibMarkup2SphinxConverter.

Introduction: RTEMS uses the Newlib C Library for a significant portion of its POSIX support. Currently, the RTEMS POSIX Users Guide will not provide documentation for a method not based on Newlib's. Therefore, this project aims to automatically convert Newlib markup to Sphinx output and integrate with POSIX users guide.

```
usage: gen_rst_from_makedoc.py [-h] [-c C_FILE_PATH] [-r RST_FILE_PATH]

Convert newlib style markup to rst markup

optional arguments:
  -h, --help            show this help message and exit
  -c C_FILE_PATH, --c_file_path C_FILE_PATH
                        Path of c source file with newlib style comments
  -r RST_FILE_PATH, --rst_file_path RST_FILE_PATH
                        Path of destination file with rst markup
```

Example invocation:

```
./gen_rst_from_makedoc.py -c ../newlib-cygwin/newlib/libc/string/strcmp.c -r example_rst.rst
```

#! /usr/bin/env python

import sys
import os.path
from optparse import OptionParser
from pyjaco import Compiler

# FIXME: This hardcoding is undesirable
if os.path.exists("py-builtins.js"):
    path_library = "py-builtins.js"
else:
    path_library = "/usr/share/pyjaco/py-builtins.js"

def compile_file(infile, outfile, options):
    '''Compile a single python file object to a single javascript output file
    object'''
    if options.builtins == "include":
        with open(path_library) as library_file:
            builtins = library_file.read()

        outfile.write("/*%s*/\n" % "  Standard library  ".center(76, "*"))
        outfile.write(builtins)
        outfile.write("/*%s*/\n" % "  User code  ".center(76, "*"))
    elif options.builtins == "import":
        outfile.write('load("%s");\n' % path_library)

    c = Compiler()
    c.append_string(infile.read())
    outfile.write(str(c))

def main():
    parser = OptionParser(usage="%prog [options] filename",
                          description="Python to JavaScript compiler.")

    parser.add_option("-o", "--output",
                      action = "store",
                      dest   = "output",
                      help   = "write output to OUTPUT, can be a file or directory")

    parser.add_option("-b", "--builtins",
            action = "store",
            dest = "builtins",
            choices = ["include", "import", "generate", "none"],
            default = "none",
            help = "INCLUDE builtins statically in each file\nIMPORT builtins using a load statement in each file\nGENERATE a separate file for builtins (output must be a directory)\nNONE don't include builtins")

    options, args = parser.parse_args()

    if len(args) == 1:
        filename = args[0]

        if options.output:
            if os.path.isdir(options.output):
                output_filename = os.path.splitext(os.path.basename(filename))[0]
                output_filename += ".js"
                output = open(os.path.join(options.output, output_filename), "w")
            else:
                output = open(options.output, "w")
        else:
            output = sys.stdout

        if options.builtins == "generate":
            if not options.output or not os.path.isdir(options.output):
                parser.error("--builtins=generate can only be used if --output is a directory")

            builtin_filename = os.path.join(options.output, "py-builtins.js")
            with open(builtin_filename, "w") as builtin_output:
                with open(path_library) as builtin_input:
                    builtins = builtin_input.read()
                builtin_output.write(builtins)

        with open(filename) as input:
            compile_file(input, output, options)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()

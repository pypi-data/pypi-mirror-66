/* The MIT License
 *
 * Copyright (C) 2010 Floris Bruynooghe
 *
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 */

/** Program to test linux bodged command lines
 *
 * This program re-writes it's own argv but will do so incorrectly: it will
 * not be NULL terminated.  This apperently happens in the wild.  The
 * /proc/pid/cmdline will be set to "xx" with no trailing NULL.
 *
 * What you need to do for this is clobber the last NULL (with something else
 * but a NULL) of the original argv and then write a string ending with a NULL
 * character in the space of argv.
 *
 * If this string (including NULL) is exaxtly the same length as the original
 * argv then /proc/pid/cmdline will correctly end with a NULL.  If it is a
 * different length cmdline will stop at the first argument and not include a
 * NULL.  Note that if it is longer you will be over-writing environment
 * variables (or worse if you keep writing for long enough).
 *
 * I'm tempted to think this exact behaviour is a bug in the /proc
 * code of the Linux kernel actually.
 */


#include <stdio.h>
#include <string.h>


int
main(int argc, char **argv)
{
    char *p;
    int l;
    int i;

    for (i = 0; i < argc; i++)
        if (i == 0 || p + 1 == argv[i])
            p = argv[i] + strlen(argv[i]);
    l = p - argv[0];
    p = argv[0];
    for (i = 0; i < 2; i++)
        *p++ = 'x';
    *p++ = '\0';
    for (i = 3; i < l+1; i++)
        *p++ = 'y';

    printf("%ld\n", (long)getpid());
    fflush(stdout);

    for (i = 0; i < 60; i++)
        sleep(10);
    return 0;
}

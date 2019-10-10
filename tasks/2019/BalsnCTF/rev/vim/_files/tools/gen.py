import string
import sys
import numpy as np


M = 4 # Matrix size
flag = 'Balsn{kkjjhlhlba_master}'

# XXX: `th1s` is not typo, it needs to be `1` to make the matrix non-singular.
banner = """
Welcome to th1s flag checker written in vim script.
Enter the flag in Balsn{.+} format and then press <Enter>.

This script is tested with vim 8.0.1453 + default vimrc (ubuntu 18.04).
If it runs very slow, try to disable X11 forwarding before launching vim.
It should terminate in 30 seconds.
""".strip().replace('\n', '\\n')


def output(*args):
    print(''.join(args), end='')
    return
    args = ['"%s"' % a for a in args]
    s = ' . '.join(args)
    print('    \\ %s .' % s)

print("""
fun! Banner ()

exe "norm! ggdGi%s\\n\\n>\\ "
starti
call cursor(line('.'), col('.') + 1)
inoremap <CR> <Esc>:call Check()<CR>

endfun

call Banner()

fun! Check ()
""" % banner)

# print("""
# try
# exe "norm! " . \
# """)

print('try')
print('exe "norm! ', end='')

def humanize():
    print("""
norm! G
let n = line('.')
norm! gg
while n >= 0
    norm! $
    if expand("<cword>") != ""
        exe "norm! cc" . (col('.') - 1)
    endif
    let n -= 1
    norm! j
endwhile
    """)

regPointer = 'Z'
def push(reg):
    """
    Save register
    Arg: None
    FArg: reg (Register name)
    Return: None
    FReturn: None
    """

    global regPointer
    assert( regPointer >= 'A' )
    output('`%sm%s' % (reg, regPointer))
    regPointer = chr(ord(regPointer) - 1)


def pop(reg):
    """
    Restore register
    Arg: None
    FArg: reg (Register name)
    Return: None
    FReturn: None
    """

    global regPointer
    regPointer = chr(ord(regPointer) + 1)
    assert( regPointer <= 'Z' )
    output('`%sm%s' % (regPointer, reg))


def ret(reg):
    """
    Return register
    Arg: None
    FArg: reg (Register name)
    Return: None
    FReturn: None
    """

    output('`%sma' % (reg,))


def mov(dst, src):
    """
    Move register
    Arg: None
    FArg: dst (Dest register name), src (Source register name)
    Return: None
    FReturn: dst (Dest register name)
    """

    output('`%sm%s' % (src, dst))
    return dst


def jmp(reg):
    """
    Move cursor to reg
    Arg: None
    FArg: reg (Register name)
    Return: None
    FReturn: None
    """

    output('`%s' % reg)


def declFunc(args='', local=''):
    """
    Decorator for prologue and epilogue
    FArg: args (Args register), local (Saved registers)
    FReturn: decorator
    """

    def decorator(func):

        def wrapper(*fargs, **fkwargs):

            global regPointer

            regs = args + local

            # Save registers
            for r in regs:
                push(r)

            # Set args
            ptr = ord(regPointer) + len(regs) + 1
            for i, r in enumerate(args):
                mov(r, chr(ptr+i))

            ret = func(*fargs, **fkwargs)

            # Restore registers
            for r in reversed(regs):
                pop(r)

            # Pop args
            regPointer = chr(ord(regPointer) + len(args))

            return ret or 'a'

        return wrapper

    return decorator


@declFunc()
def padd(dst, src, n):
    """
    Pointer addition: dst = src + n
    Arg: None
    FArg: dst (Dest register name), src (Source register name)
    FArg: n (number to add)
    Return: None
    FReturn: dst (Dest register name)
    """

    if n > 0:
        output('`%s%djm%s' % (src, n, dst))
    elif n < 0:
        output('`%s%dkm%s' % (src, -n, dst))
    else:
        output('`%sm%s' % (src, dst))
    return dst



@declFunc()
def alloc():
    """
    Allocate buffer
    Arg: None
    FArg: None
    Return: pointer @ a
    FReturn: pointer register
    """

    output('Go\\<esc>ma')


@declFunc()
def free(pointer):
    """
    Free buffer
    Arg: None
    FArg: pointer
    Return: None
    FReturn: None
    """

    jmp(pointer)
    output('V}d') # Delete array
    output('ggm%s' % pointer) # Clear pointer


@declFunc(args='b')
def clone():
    """
    Clone array
    Arg: array
    Return: cloned array
    """

    jmp('b')
    output('V}yGpma')


@declFunc()
def append(dst, src):
    """
    Append one element from dst to src
    Arg: None
    FArg: dst, src
    Return: None
    FReturn: None
    """

    jmp(src)
    output('yy')
    jmp(dst)
    output('P')


@declFunc()
def pToHead(reg):
    """
    Change array pointer to head
    Arg: None
    FArg: reg (Register name)
    Return: None
    FReturn: None
    """

    output('`%s{jm%s' % (reg, reg))


@declFunc(args='b', local='c')
def toNumber(start, end):
    """
    Convert string from start to end to array
    Arg: None
    FArg: start, end
    Return: array [start-end]
    FReturn: array register
    """

    mov('c', alloc())
    jmp('b')
    output(':exe \\"let g:l=getline(\'.\')\\"\\<cr>')
    jmp('c')
    for i in range(start, end):
        output('o\\<esc>')
        output(':exe \\"norm! \\".(strgetchar(g:l[%s:], 0) %% 32 + 1).\\"ax\\"\\<cr>' % i)
        output('^rX')
    output('o\\<esc>') # Terminate array
    jmp('c')
    output('J') # Remove empty line
    ret('c')


@declFunc(args='b', local='cd')
def transpose(n):
    """
    Matrix transpose
    Arg: mat @ b [n x n]
    FArg: n
    Return: mat.T [n x n]
    FReturn: None
    """

    mov('c', alloc()) # allocate output buffer
    for x in range(n):
        mov('d', 'b') # d = iter(mat)
        for y in range(n):
            append('c', 'd')
            if y != n-1:
                padd('d', 'd', n)
        if x != n-1:
            padd('b', 'b', 1)
    pToHead('c')
    ret('c')


@declFunc(args='bc', local='d')
def add():
    """
    Scalar addition
    Arg: num1 @ b, num2 @ c
    Return: num1 + num2
    """

    mov('d', alloc())
    append('d', 'b') # Copy operands
    append('d', 'c') # Copy operands
    pToHead('d')
    jmp('d')
    output('Jxx^x') # Add
    output(':s/\\\\(x\\\\{32}\\\\)*//g\\<cr>') # mod 32
    output('IX\\<esc>')
    ret('d')


@declFunc(args='bc', local='de')
def mul():
    """
    Scalar multiplication
    Arg: num1 @ b, num2 @ c
    Return: num1 * num2
    """

    mov('d', alloc())
    append('d', 'b') # Copy operands
    output('`dOX\\<esc>me') # Result line
    pToHead('d')
    jmp('d')
    output('x')
    for _ in range(32):
        append('e', 'c')
        jmp('d')
        output('vyjPxxVy') # copy((d > 0) * c)
        output('`epkJx') # e += (d > 0) * c
        output('`dx') # d = max(0, d-1)
        output('jV`ekd') # clear tmp
        output('`ex') # remove X
        output(':s/\\\\(x\\\\{32}\\\\)*//g\\<cr>') # mod 32
        output('IX\\<esc>') # insert head
        # output(':redraw\\<cr>')
    jmp('d')
    output('J') # clear d
    ret('d')


@declFunc(args='b', local='c')
def ishl(n):
    """
    Logical shift left immediate
    Arg: num1 @ b
    FArg: num2
    Return: num1 << num2
    """

    assert( n > 0 )
    push('b')
    push('b')
    mov('b', add())

    for _ in range(n-1):
        push('b')
        push('b')
        mov('c', add())
        free('b')
        mov('b', 'c')

    ret('b')


@declFunc(args='b', local='c')
def ishr(n):
    """
    Logical shift right immediate
    Arg: num1 @ b
    FArg: num2
    Return: num1 >> num2
    """

    assert( n > 0 )
    mov('c', alloc())
    append('c', 'b') # Copy operands
    pToHead('c')
    jmp('c')
    output('x') # Remove X
    for _ in range(n):
        output('axx\\<esc>') # c += 2
        output(':s/^\\\\(\\\\%(xx\\\\)*\\\\)x\\\\?$/\\\\1/g\\<cr>') # c -= c % 2
        output(':s/xx/x/g\\<cr>') # c /= 2
        output('x') # c -= 1
    output('IX\\<esc>') # Add X

    ret('c')


@declFunc(args='b', local='cde')
def iror(n):
    """
    Logical rotate right immediate
    Arg: num1 @ b
    FArg: n
    Return: (num1 >> n) | (num1 << (5 - n))
    """

    push('b')
    mov('c', ishr(n))

    push('b')
    mov('d', ishl(5 - n))

    push('d')
    push('c')
    mov('e', add())
    free('d')
    free('c')

    ret('e')


@declFunc(args='b', local='cde')
def irol(n):
    """
    Logical rotate left immediate
    Arg: num1 @ b
    FArg: n
    Return: (num1 << n) | (num1 >> (5 - n))
    """

    push('b')
    mov('c', ishl(n))

    push('b')
    mov('d', ishr(5 - n))

    push('d')
    push('c')
    mov('e', add())
    free('d')
    free('c')

    ret('e')


@declFunc(args='b', local='d')
def psum(n):
    """
    Sum all elements in a vector
    Arg: num1[n] @ b
    FArg: n
    Return: sum(num1)
    """

    push('b')
    mov('d', clone())
    jmp('d')
    output('Jxx' * (n-1)) # Sum
    output(':s/\\\\(x\\\\{32}\\\\)*//g\\<cr>') # mod 32
    ret('d')


@declFunc(args='bc', local='de')
def pmul(n):
    """
    Vector multiplication
    Arg: num1[n] @ b, num2[n] @ c
    FArg: n
    Return: num1 * num2
    """

    mov('d', alloc())
    for i in range(n):
        push('b')
        push('c')
        mov('e', mul())
        append('d', 'e')
        free('e')
        if i != n-1:
            padd('b', 'b', 1)
            padd('c', 'c', 1)
    pToHead('d')
    ret('d')


@declFunc(args='bc', local='de')
def dot(n):
    """
    Vector inner product
    Arg: num1[n] @ b, num2[n] @ c
    FArg: n
    Return: num1 * num2
    """

    mov('d', alloc())
    for i in range(n):
        push('b')
        push('c')
        mov('e', mul())
        append('d', 'e')
        free('e')
        if i != n-1:
            padd('b', 'b', 1)
            padd('c', 'c', 1)
    pToHead('d')
    jmp('d')
    output('Jxx' * (n-1)) # Sum
    output(':s/\\\\(x\\\\{32}\\\\)*//g\\<cr>') # mod 32
    ret('d')


@declFunc(args='bc', local='defg')
def matmul(n):
    """
    Matrix multiplication
    Arg: a @ a (nxn), b @ b (nxn)
    Return: matmul(a, b) @ a (nxn)
    """


    mov('d', alloc())
    push('c')
    mov('e', transpose(n))

    # Multiply
    for y in range(n):
        mov('f', 'e') # f = iter(e)
        for x in range(n):
            push('f')
            push('b')
            mov('g', dot(n))
            append('d', 'g')
            free('g')
            if x != n-1:
                padd('f', 'f', n)
        if y != n-1:
            padd('b', 'b', n)
    free('e')
    pToHead('d')
    ret('d')


@declFunc(args='bc', local='defg')
def encryption(n):
    """
    Encryption
    Arg: key[n] @ b, plainText[n] @ c
    FArg: n
    Return: cipherText[n]
    """

    mov('d', alloc())
    jmp('d')
    output('OX\\<esc>')

    for i in range(n):
        padd('e', 'd', -1) # e = last(d)

        push('b')
        mov('f', iror(2))

        push('c')
        mov('g', iror(2))

        push('e')
        push('f')
        mov('e', add())
        free('f')

        push('e')
        push('g')
        mov('f', add())
        free('e')
        free('g')

        append('d', 'f')
        # output(':redraw\\<cr>')

        free('f')

        padd('b', 'b', 1)
        padd('c', 'c', 1)

    pToHead('d')
    output('xJ') # Remove padding
    ret('d')


@declFunc(args='b', local='c')
def icmp(val):
    """
    Compare array immediate
    Arg: key[len(val)] @ b
    FArg: val[..]
    Return: bool
    """

    push('b')
    mov('c', clone())
    jmp('c')
    for v in val:
        output(':s/X\\\\(x\\\\{%d}\\\\)\\\\?/X/g\\<cr>' % v) # compare
        output(':s/X\\\\(x\\\\?\\\\)x*/X\\\\1/g\\<cr>') # to bool
        output('j') # next
    jmp('c')
    output('Jxx' * (len(val)-1)) # join
    output(':s/X\\\\(x\\\\?\\\\)x*/X\\\\1/g\\<cr>') # to bool


# Main

def main():
    global flag, banner, key, cipher

    banner = banner.replace(' ', '_').split('\\n')
    output('gg' + 'Jx' * (len(banner))) # join
    banner = ''.join(banner).ljust(M*M, '\0')[:M*M]
    output('^%dld$' % (M*M)) # trim banner
    output(':s/ /_/g\\<cr>') # replace space

    flag = flag[len('Balsn{'):-len('r}')].ljust(M*M, '\0')
    output('j')
    output(':s/^> Balsn{\\\\([a-z_]\\\\+\\\\)r}$/\\\\1/g\\<cr>')
    output(':%s/\\\\n//g\\<cr>') # join

    # ROT13
    def rot13(s):
        x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        y = 'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        d = {xi: yi for xi, yi in zip(x,y)}
        return ''.join(d.get(c, c) for c in s)

    flag = rot13(flag)
    banner = rot13(banner)
    output('^v$g?')

    # Insert margin
    output('O\\<esc>jo\\<esc>')

    # Clear all registers
    output('ggm' + 'm'.join(string.ascii_lowercase))

    # Read input
    output('ggjmb')

    # Convert to number
    flag = np.array([ord(c) % 32 for c in flag]).reshape(M, M)
    key = np.array([ord(c) % 32 for c in banner]).reshape(M, M)
    push('b')
    mov('c', toNumber(0, M*M)) # key
    push('b')
    mov('d', toNumber(M*M, M*M*2)) # input
    free('b')
    mov('b', 'c')
    mov('c', 'd')

    # Generate key
    key = (key @ key) % 32
    push('b')
    push('b')
    mov('d', matmul(M))
    # push('b')
    # mov('d', clone())

    # Mix plaintext
    flag = (key @ flag) % 32
    push('c')
    push('d')
    mov('e', matmul(M))
    # push('c')
    # mov('e', clone())

    # Encrypt
    flag = flag.flatten()
    key = key.flatten()
    cipher = []
    e = 0
    for k, f in zip(key, flag):
        e = ((k >> 2) + (k << 3) + (f >> 2) + (f << 3) + e) % 32
        cipher.append(e)

    push('e')
    push('d')
    mov('f', encryption(M*M))

    # Compare to answer
    push('f')
    mov('g', icmp(cipher))

    # Clean
    free('b')
    free('c')
    free('d')
    free('e')
    free('f')

    # Output result
    jmp('g')
    output('kddjdd') # remove margin
    output(':s/^X$/Correct/g\\<cr>')
main()



# End
# print("""\
    # \\ ""
# """)
print('"')

print("""\
catch
    norm! ggdGiWrong
endtry
""")

# Debug - to number
# humanize()

print("""
endfun
""")
# import sys
# print(key, file=sys.stderr)
# print(cipher, file=sys.stderr)

import sys
import random
import functools as fn


prefix = f'L{random.randrange(1000000)}'
with open(sys.argv[1], 'r') as f:
    code = f.read()
    code = [l.strip() for l in code.split('\n')]
    code = [l for l in code if l]


#-- Remove garbages --#
code = [l for l in code if not l.startswith('.file')]
code = [l for l in code if not l.startswith('.cfi')]
code = [l for l in code if not l.startswith('.ident')]


#-- Collect global and type tags --#
globl = [l for l in code if l.startswith('.globl')]
code = [l for l in code if not l.startswith('.globl')]

tipe = [l for l in code if l.startswith('.type')]
code = [l for l in code if not l.startswith('.type')]


#-- Group sections --#
SECSTR = {'.text': 1, '.bss': 1, '.data': 1}
sec, sections = "", {"": []}
for line in code:
    if line.startswith('.section') or line in SECSTR:
        sec = line
        if sec not in sections:
            sections[sec] = [line]
    else:
        sections[sec].append(line)


#-- Stick labels --#
text, labels = [], []
for line in sections['.text']:
    labels.append(line)
    if not line.endswith(':'):
        text.append(labels)
        labels = []


#-- Remove size --#
text = [b for b in text if not b[-1].startswith('.size')]


#-- Insert jmpaddr variable --#
tipe.append(f'.type   {prefix}_jmpaddr, @object')
sections['.bss'].append(f'.size   {prefix}_jmpaddr, 16')
sections['.bss'].append(f'{prefix}_jmpaddr:')
sections['.bss'].append(f'.zero   16')
tipe.append(f'.type   {prefix}_r14, @object')
sections['.bss'].append(f'.size   {prefix}_r14, 8')
sections['.bss'].append(f'{prefix}_r14:')
sections['.bss'].append(f'.zero   8')
tipe.append(f'.type   {prefix}_r15, @object')
sections['.bss'].append(f'.size   {prefix}_r15, 8')
sections['.bss'].append(f'{prefix}_r15:')
sections['.bss'].append(f'.zero   8')


#-- Glue --#
for i, block in enumerate(text):
    block.insert(0, f"""
    {prefix}_GLUE{i}:
    movq 0+{prefix}_r14(%rip), %r14;
    movq 0+{prefix}_r15(%rip), %r15;
    """)
    block.append(f"""
    movq %r14, 0+{prefix}_r14(%rip);
    movq %r15, 0+{prefix}_r15(%rip);
    lea 42+{prefix}_GLUE{i + 1}(%rip), %r15;
    movq %r15, 0+{prefix}_jmpaddr(%rip);
    movq $42+{prefix}_JMPOUT, %r15;
    movq %r15, 8+{prefix}_jmpaddr(%rip);
    jmp {prefix}_JMPOUT;
    """)
text.append([f"""
{prefix}_GLUE{len(text)}:
{prefix}_JMPOUT:
    movq 0+{prefix}_jmpaddr(%rip), %r14;
    movq 8+{prefix}_jmpaddr(%rip), %r15;
    lea -42(%r14), %r14;
    lea -42(%r15), %r15;
    xchg %r14, %r15;
    movq %r14, 0+{prefix}_jmpaddr(%rip);
    movq %r15, 8+{prefix}_jmpaddr(%rip);
    jmp *%r15;
    """])


#-- Reduce --#
#-- Disabled to make it slightly easiler --#
# for block in text[:-1]:
    # cmd = block[-2]
    # if cmd.startswith('jmp') or cmd.startswith('ret'):
        # block.pop()


#-- Shuffle --#
random.shuffle(text)


#-- Flatten text --#
text = [l for b in text for l in b]
sections['.text'] = text


#-- Add a fake flag --#
sections['.section\t.rodata'].append(
    '.string "AIS3{'
    'WH3N_d0_y0u_H4v3_tH3_impr355i0N_tH4t_'
    'tHi5_cH4113Ng3_c4N_b3_501v3d_by_5triNg5_!?!?'
    '}"'
    )


#-- Output code --#
code = fn.reduce(lambda l, x: l + x, sections.values())
code = globl + tipe + code
for line in code:
    print(line)

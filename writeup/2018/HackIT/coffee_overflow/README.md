# Task Info
coffee_overflow - rev 1000 - 1 solve  
Our mobile developer has severe coffee overflow, and lost password to his own app. Please help him to recover.  

## Hints
Do you have any idea how to ede?  
How it may be connected with IDEA? EDE is also not only the city in Netherlands.  

## Time
20 hours, a little bit crazy...

# Solution
This is a java reverse challenge with obfuscation.
I'll try to write down the whole process how I reverse it,
it is a little bit lengthy.
You'll see how I defeat those obfuscation techniques in detail.


## TL;DR
* Rename the spaces.
* Fix the signature.
* Decrypt the string constants.
* Recover the function name of InvokeDynamic
* Recover the integer constants.
* Read the bytecode, the bytecode, and the bytecodes.
* Decrypt the flag

## Program's behavior
Execute it without argument gives me:
```
i can haz password? usage: <me> password
```
But it still output the same message even if I pass some arguments to it...


## Get started
Every Java reverse challenge starts with opening it using `jd-gui`.
The name of class, method, field are obfuscated,
and there's some internal error when decompiling.

Open it with editor you can find a string
"Obfuscation by Radon obfuscator developed by ItzSomebody"
at the bottom.
Searching for a deobfuscator for Radon but didn't found anything.

Ok, let's try some other decompilers like `CFR`, `Luyten(Procyon)` ...
And none of them worked.

How about disassembler?
`Bytecode Viewer` seems works,
at least it shows some bytecode.


## Fix the names
The output of bytecode viewer is not very readable:
the names are composed of many unicode spaces (U+2000 ~ U+200f),
they are not distinguishable.

Those spaces in utf8 is `E2 80 8x`,
so I replaced them with `_x_` to create unique, distinguishable and legal identifier names.
Jar is actually a zip file, you have to unzip to modify the files in it.

Here's my [script](rename.py) to walk through all the files and change their filename and content.

Great, after packing it back to jar and opening with bytecode viewer,
we produce some bytecodes that is readable.

Before we start dig into the bytecode,
let's see a special file named `META-INF/MANIFEST.MF` in the jar.
```
Manifest-Version: 1.0
Created-By: 1.7.0_06 (Oracle Corporation)
Main-Class: _9__6__c__d__f__3__5__d__0__0_._7__9__6__f__f__7__e__3__e__f_
```
It specify where the entry point is.

I can find the file named `96cd.../796f....class` in the jar,
but it's not in my bytecode viewer.
Drag the classfile into bytecode viewer gives me `java.lang.IllegalArgumentException`.

What's going wrong??


## Fix the signature
After trying other disassembler,
I found `javap` (a disasm tool in JDK) reports an interesting error:
```
Error: A serious internal error has occurred: java.lang.IllegalStateException: !_!b__a__2__2__4__8__b__4__5__6_
Please file a bug report, and include the following information:
java.lang.IllegalStateException: !_!b__a__2__2__4__8__b__4__5__6_
        at jdk.jdeps/com.sun.tools.classfile.Signature.parseTypeSignature(Signature.java:180)
        at jdk.jdeps/com.sun.tools.classfile.Signature.parse(Signature.java:104)
        at jdk.jdeps/com.sun.tools.classfile.Signature.getType(Signature.java:48)
        at jdk.jdeps/com.sun.tools.javap.ClassWriter.write(ClassWriter.java:219)
        at jdk.jdeps/com.sun.tools.javap.JavapTask.write(JavapTask.java:836)
        at jdk.jdeps/com.sun.tools.javap.JavapTask.writeClass(JavapTask.java:655)
        at jdk.jdeps/com.sun.tools.javap.JavapTask.run(JavapTask.java:600)
        at jdk.jdeps/com.sun.tools.javap.JavapTask.run(JavapTask.java:450)
        at jdk.jdeps/com.sun.tools.javap.Main.main(Main.java:47)
```
What is a valid signature?
I found some CFG in [JVM doc](https://docs.oracle.com/javase/specs/jvms/se10/html/jvms-4.html#jvms-4.7.9.1)
about the signature.
And `Lxxx;` seems to be a valid signature.
I replace the signature using hex editor, and now `javap` can disassemble it!!!

Bytecode viewer still crashed,
so I disassemble all the classfile with `javap`,
and start to work with them using Sublime text.

Also, when editing the signature, I found a string `RADON0.8.2`,
which tells me about the version of obfuscator.


## Decrypt string constants
After looking around the bytecode, I found a interesting part at the beginning.
```
64: invokedynamic #45,  0             // InvokeDynamic #1:_3__7__d__e__1__a__3__0__e__1_:()Ljava/io/PrintStream;
69: iconst_0
70: invokestatic  #49                 // Method _8__1__8__6__a__1__b__c__6__e_:(I)Ljava/lang/String;
73: aconst_null
74: ldc           #50                 // int 37329
76: invokestatic  #54                 // Method _d__7__b__5__e__2__f__a__f__c_._9__e__f__1__c__0__6__5__1__7_:(Ljava/lang/Object;Ljava/lang/Object;I)Ljava/lang/String;
```
I can't find `37de...` appears in other places,
but let's ignore it now.

Hmm, `PrintStream`... It seems going to output something.
`8186...` is a function at the bottom,
which takes a index and return a garbled string in its string table.
Also, in every place `8186...` is called,
the return string are always passed into `d7b5.../9ef1...` and return another string.

A string table and a function decrypt it?
Looks like how obfuscator works.
After digging into Radon's source code, I found that `9ef1...` looks like
[Normal String Encryption](https://github.com/ItzSomebody/Radon/blob/0.8.2/src/main/java/me/itzsomebody/radon/templates/NormalStringEncryption.java)
based on the functions they called.
Their source code is obfuscated, [Here's](radonMethods) the code after cleaning up.

The encryption is actually single char xor.
I'm too lazy to calculate the key,
so I just brute all the 256 keys and chose the best one manually.
All the five strings in entry classfile is:
```
i can haz password? usage: <me> password
rabbit hole
nice kitten
mad dog!
the winrar is u! subit password as flag!
```

Next, let's deal with dynamic invocation.


## Recover Dynamic Invocation
Invoke dynamic works like PLT in C binary.
It will call a resolver that will return the correct function first.
The difference is that we can provide our own resolver and its argument.
If you run `javap` with verbose switch on, it will output this at the bottom:
```
BootstrapMethods:
  0: #21 REF_invokeStatic _d__7__b__5__e__2__f__a__f__c_._5__a__e__3__9__2__6__4__a__8_:(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    Method arguments:
      #22 1
      #23 0
      #25 ????????????????
      #27 ??????
      #29 ???
  1: #21 REF_invokeStatic _d__7__b__5__e__2__f__a__f__c_._5__a__e__3__9__2__6__4__a__8_:(Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    Method arguments:
      #23 0
      #22 1
      #37 ????????????????
      #39 ???
      #41 ???????????????????
```

It tells me that `d7b5.../5ae3...` is the resolver.
In the same folder of radon's string encryption source code,
there are some filename contains `InvokeDynamic`.
It seems to be [Heavy Invoke Dynamic](https://github.com/ItzSomebody/Radon/blob/0.8.2/src/main/java/me/itzsomebody/radon/templates/HeavyInvokeDynamic.java) based on the switch statment they use.

It encrypt className with single char xor using 4382, memberName using 3940, and descriptor using 5739.

Here's the [script](invokeSolver.py) to put the correct function name in its comment.

Now, previous snippet about the print looks like:
```
64: invokedynamic #45,  0             //  InvokeDynamic #1: java.lang.System/out:java.io.PrintStream
69: iconst_0
70: invokestatic  #49                 // Method "8__1__8__6__a__1__b__c__6__e__":(I)Ljava/lang/String;
73: aconst_null
74: ldc           #50                 // int 37329
76: invokestatic  #54                 // Method d__7__b__5__e__2__f__a__f__c__."9__e__f__1__c__0__6__5__1__7__":(Ljava/lang/Object;Ljava/lang/Object;I)Ljava/lang/String;
79: invokedynamic #64,  0             //  InvokeDynamic #2: java.io.PrintStream/println:(Ljava/lang/String;)V
```
Looks much better, right?


## Recover integer constants
There are many bytecode have following pattern:
```
46: ldc           #34                 // int 814620811
48: ldc           #35                 // int 814620819
50: ixor
```
The answer is 24, that's how radon obfuscate integer constants.
Here's the [script](processXor.py) calculate the result and put in its comment.
Now, it looks like:
```
34: aload_0
35: ldc           #14                 // int 530953560
37: ldc           #14                 // int 530953560
39: ixor                              // eql 0
40: aaload
41: invokedynamic #33,  0             // InvokeDynamic #0: java.lang.String/length:()I
46: ldc           #34                 // int 814620811
48: ldc           #35                 // int 814620819
50: ixor                              // eql 24
51: if_icmpeq     102
```
Great, I can understand the bytecode now: It check that the first argument should be 24 chars long.


## Human decompiler
We have all the pieces now. It's time to spent 8hr reading the bytecodes :)

Here's some tips to read them:

#### Where to read?
Most of file/function is not used in the program due to the nature of java.
You may better read the code along its exection flow (either reversed or forward).

#### Useless prologue
All the function starts with something like this:
```
0: getstatic     #11                 // Field b__5__7__3__a__4__4__b__3__3__:Z
3: istore        6
5: goto          9
8: return
```
It's useless, just remove it.

#### Nop on statement boundary
There a lot of code like this in everywhere:
```
 9: iload         6
11: ifne          8
14: iload         6
16: ifne          8
```
It's also useless, but you may better left a newline when you replace it.
It's a awesome boundary that can help you split the bytecode into smaller fragments.

#### Jump and loop
When you see something like:
```
 84: iload         6
 86: ifne          8
 89: iload         6
 91: iconst_0
 92: if_icmpeq     837
 95: aconst_null
 96: athrow
 97: nop
 98: nop
 99: nop
100: nop
101: athrow
```
It's actually `jmp 837`.
It may be a if-else clause or a while/for loop, depending on the jumping direction.

#### Store
Store commands (`istore`, `iastore`, `bastore`) are also great boundaries too.
Psuedo code of each fragments will looks like `reg5 = a * b(4) + 1`


## Decrypt the flag
Here's the psuedo code I recovered:
```java
public class MainPackage.MainClass extends java.lang.Object {
  public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    Code:
        if len(argv) != 1 and len(argv[0]) == 24:
            print("i can haz password? usage: <me> password")
        pwd = new PasswordEncryptor("rabbit hole") // IDEA Cipher
        inp2 = argv[0].getBytes()
        inp3 = argv[0].getBytes()
        pwd.setKey("nice kitten")
        pwd.decrypt(inp2, 0, inp3, 0) // input, offset, output, offset
        pwd.encrypt(inp2, 8, inp3, 8)
        pwd.decrypt(inp2, 16, inp3, 16)
        pwd.setKey("mad dog!")
        pwd.encrypt(inp3, 0, inp2, 0)
        pwd.decrypt(inp3, 8, inp2, 8)
        pwd.encrypt(inp3, 16, inp2, 16)

        target = [
            153, 2, 87, 234, 183, 183, 247, 180, 39, 34, 57,
            6, 159, 247, 124, 43, 8, 5, 45, 45, 12, 15, 199, 25]

        for a, b in zip(target, inp2):
            if a != b:
                return
        print("win")
```
Hey bro, its NOT EDE mode...
In 3DES, EDE mode is `Enc(Dec(Enc(msg, k1), k2), k3)` which makes the key 3 times longer.
I double checked the bytecode, but didn't found any mistake.

I wrote a script to use PyCrypto's IDEA Cipher to decrypt the flag, but failed.
I checked the bytecode third time, but still didn't found any mistake.
The nightmare begins now.
I thought the author may modified the algorithm,
so I spent another 4 hours recovering all the details of its IDEA algorithm.
and 2 hours debugging my decryption algorithm.

I'll skip the part of reversing, let's talk about how I debug the code.


## Debug
I very surprised that there's no bytecode level debugger like gdb in JDK. 
I've tried some debuggers:
* I have totally no idea how to use jbcd.
* Bytecode Viewer can't open some of the classfiles
* Some debugger is too fat that I want to avoid. (e.g. plugin of eclipse)

So I go with a different approach: write another java program to import the classfile.
Unicode are legal identifiers in java (you may need to compile with `javac -encoding utf8`).
When I tried to compile this code:
```java
import   ‌‍‏  ‍  .   ‏‏ ‎ ‎‏; // These spaces means PasswordEncryptor in the pseudo code above
// test.java:1: error: illegal character: '\u200f'
```
How about running the renamer above to change the name?
Here the error message:
```java
import _0__3__5__6__6__2__2__9__1__b_._2__5__4__e__4__4__9__5__7__1_;
...
  _2__5__4__e__4__4__9__5__7__1_ encryptor = new _2__5__4__e__4__4__9__5__7__1_("nice kitten");
...

/*
test.java:22: error: cannot find symbol
        _2__5__4__e__4__4__9__5__7__1_ encryptor =      new _2__5__4__e__4__4__9__5__7__1_("nice kitten");
                                                        ^
  symbol:   constructor _2__5__4__e__4__4__9__5__7__1_(String)
  location: class _2__5__4__e__4__4__9__5__7__1_
test.java:25: error: cannot access b__3__6__e__6__0__a__f__d__1
        printarr(encryptor._c__2__c__0__a__9__0__f__1__4_, 52, 6);
                          ^
  class file for b__3__6__e__6__0__a__f__d__1 not found
*/
```
`b36e...` is the signature of that classfile, where it should point to its superclass.
After fixing the signature, it still complains that it can't find the constructor.

I have no idea how to fix the classfile.
I use another hacky method to come over this problem.
Create a placeholder package which has same interface as our target:
```java
package _0__3__5__6__6__2__2__9__1__b_;
public class _2__5__4__e__4__4__9__5__7__1_ extends Object {
    public int[] _a__f__8__d__e__a__1__c__9__3_;
    public int[] _c__2__c__0__a__9__0__f__1__4_;

    public _2__5__4__e__4__4__9__5__7__1_(String key) {
        this._a__f__8__d__e__a__1__c__9__3_ = new int[52];
        this._c__2__c__0__a__9__0__f__1__4_ = new int[52];
    }

    public void _3__0__7__8__8__0__f__9__6__9_(byte[] inp, int offInp, byte[] out, int offOut) {
    }

    public static int _1__6__7__e__5__4__f__7__a__b_(int a, int b) {
        return 0;
    }
}
```
After compiling our code, substitute spaces for `_x_` back (See [this script](renameBack.py))
and it will call the function I want.
Now, I can start debugging my decryption algorithm,
or simply call the library to decrypt the flag.


# Discussion with author (@Solarwind)
* He use `acme` package for IDEA Cipher and didn't modify anything.
I not sure which implementation is wrong.
But `PyCrypto` had removed its IDEA code due to patent issue after version `2.0.2`.
* He tells me a interesting technique called `Java agent` to do instrumentation.
* `java-deobfuscator` supports for `stringer`, which has similar obfuscation techniques.
You can refer to their code to understand the way of writing a deobfuscator.

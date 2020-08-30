---
name: Remote Control
category: Hardware
points: 363
solves: 10
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> You're in the room with a TV, an IOT Hub, and a smart wall clock.
> However, the TV's remote is not in your hand but you find the TV to be noisy,
> and want to turn it off.  
> You found out that the IOT Hub is connected to the guest WiFi and its API endpoint is exposed.
> Also, you found a simple client for the wall clock through the API.  
> Find a way to turn the TV off for the flag.


## Time
3 hours  
Another Epic Guessing Challenge.


# Behavior
We can access to an endpoint `/SendIRCommand` of an IOT hub.
and their IR protocol supports several commands:

```
CMD_PING = 0x01

CMD_GETTEMP = 0x10
CMD_GETHUMIDITY = 0x11
CMD_GETCO2 = 0x12
CMD_GETSMOKEDETECTOR = 0x13

CMD_SETTIME = 0x20

CMD_SYSVER = 0x30

CMD_REPLY = 0x80
```

We only have the client to communicate with the server.
And we know nothing about the server.

Also, we know nothing about the TV, our target.


# Solution
## TL;DR
1. Guess 🤔
2. Guess again 🤔
3. Guess once again 🤔
4. Send a NEC IR message using that IOT hub.


Feel free to skip to the last section if you're not interested in how I came up with the guess.


## Guessing about the server
Without any knowledge of the server,
I start from poking the endpoint,
trying to figure out what the device is.

Similar to services in other challenges, it is hosted on GCP (europe-west1).
And the service is hidden behind Google Front End (GFE).
I didn't find anything else, it seems to be a fake IOT hub.


## Guessing about the service
We can send a IR packet in hex format to the endpoint,
and it will give us the result it received from the smart clock.

According to the client, the IR packet looks like this:
```
u8      magic byte (0x55)
u8      length of the packet including header
u8      command
u8 x n  arguments
u8      CRC8-CCITT
```

I tested all 256 commands,
but I didn't found anything interesting other than those listed in the client.

`CMD_PING` replies our argument xor `0x12 + i`, and commands larger than 0x80 simply replies what we send.
Other commands reply their predefined strings.

I also put a packet inside a packet or inside the reply, hoping it trigger something.
But nothing happened. Also the packet will be invalid after padding.

Great, I'm out of ideas.


## Guessing about the client

In the client, there are five comments. two of them are interesting:
```python
def crc8(data):
    # Expect a list of integer
    # LFSR calculation of CRC8-CCITT
    crc = 0

" ... "

# Send the request packet to the Hub to be transmitted to the smart clock
# through 940nm IR at 1786bps
req = requests.post('https://%s/%s'%(host, HUB_ENDPOINT), data=packet_hex)
```

CRC8-CCITT is used in 3DS' IR protocol, but it seems to be unrelated. 
940nm is typical wavelength of IR light, nothing interesting.

How about 1786bps?
I couldn't find any protocol works in 1786bps.
It's a pretty strange bitrate.
It's too high for a control protocol, which is typically around 4 ~ 120 bps,
and it's too low for a transmission protocol, which is typically around 10kbps ~ 1Gbps.

To test its behavior,
I spawn a GCP instance at europe-west1,
and send a 255 bytes ping packet to it.
It should takes at least `255 * 8 * 2 / 1786 = 2.3` seconds to transmit.

However, the server replies in 0.3 second.

Ahhh, it's fake, well play.
But why they write a fake comment?


## Guessing about the protocol
When searching about IR protocols online,
I notice that they mention about the length of burst.

For example, Philips RC-5 Protocol use a 889us burst following a 889us pause to represent bit 0.

I start wondering what is the length of the protocol in this task: `1bit / 1786bps = 560us`

Googling with the keyword `560us` again, and I found something promising:
[The NEC protocol](https://www.sbprojects.net/knowledge/ir/nec.php).

Its bit symbol looks like this:

![modulation]({_files/necmodulation.png})

The protocol looks like:

![protocol]({_files/nectrain.png})

It contains:
* A 9ms leading burst
* A 4.5ms pause
* The address
* The inverted address
* The message
* The inverted message
* A 560us burst at the end

I trying to believe that our IOT hub sends raw IR burst so that we can forge a NEC packet.


## Send a NEC packet
First, here's a function to build the bit symbols:
```c
def buildNECSig(cmd):
    ret = []
    for s in range(8):
        if (cmd >> s) & 1:
            ret += [1] + [0] * round(2250 / 560 - 1)
        else:
            ret += [1] + [0]
    return ret
```

Next, I build the packet according to the protocol
```python
def buildNEC(addr, cmd):
    sig = []
    sig += [1] * round(9000 / 560) # leading burst
    sig += [0] * round(4500 / 560) # leading pause
    sig += buildNECSig(addr)
    sig += buildNECSig(addr ^ 0xff)
    sig += buildNECSig(cmd)
    sig += buildNECSig(cmd ^ 0xff)
    sig += [1] # Final burst

    assert len(sig) == 121

    sz = (len(sig) + 7) // 8

    # Find the correct bit order
    # sig = int(''.join(map(str, sig)), 2).to_bytes(sz, 'big')
    # sig = int(''.join(map(str, sig)), 2).to_bytes(sz, 'little')
    # sig = int(''.join(map(str, sig[::-1])), 2).to_bytes(sz, 'big')
    sig = int(''.join(map(str, sig[::-1])), 2).to_bytes(sz, 'little')

    return sig
```

I don't know how our IOT hub convert bytes to bits, so I test all four possible ones.

To get the flag, just send a NEC packet, the value of address and command doesn't matter.

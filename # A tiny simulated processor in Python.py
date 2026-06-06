# A tiny simulated processor in Python

class SimpleCPU:
    def __init__(self):
        self.registers = [0] * 4   # 4 general-purpose registers
        self.pc = 0                # program counter
        self.memory = [0] * 256    # small memory

    def load_program(self, program):
        self.memory[:len(program)] = program

    def run(self):
        while self.pc < len(self.memory):
            instr = self.memory[self.pc]
            if instr == 1:  # ADD R0 + R1 -> R0
                self.registers[0] += self.registers[1]
            elif instr == 2:  # SUB R0 - R1 -> R0
                self.registers[0] -= self.registers[1]
            elif instr == 3:  # LOAD immediate into R0
                self.pc += 1
                self.registers[0] = self.memory[self.pc]
            elif instr == 99:  # HALT
                break
            self.pc += 1

# Example program: load 10 into R0, load 5 into R1, add them
program = [3, 10, 3, 5, 1, 99]

cpu = SimpleCPU()
cpu.load_program(program)
cpu.run()

print("Result in R0:", cpu.registers[0])
// A very simplified processor core in Verilog
module SimpleCPU (
    input clk,
    input reset,
    output reg [7:0] out
);

    reg [7:0] registerA;
    reg [7:0] registerB;
    reg [7:0] pc;          // program counter
    reg [7:0] memory [0:255]; // small memory

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            pc <= 0;
            registerA <= 0;
            registerB <= 0;
            out <= 0;
        end else begin
            case (memory[pc])
                8'h01: registerA <= registerA + registerB; // ADD
                8'h02: registerA <= registerA - registerB; // SUB
                8'h03: begin
                    pc <= pc + 1;
                    registerA <= memory[pc];               // LOAD immediate
                end
                8'hFF: out <= registerA;                   // OUTPUT
            endcase
            pc <= pc + 1;
        end
    end
endmodule
// Simplified motherboard system in Verilog
module Motherboard (
    input clk,
    input reset,
    output [7:0] io_out
);

    wire [15:0] address;
    wire [7:0] data_in, data_out;
    wire mem_read, mem_write;

    // CPU core
    SimpleCPU cpu (
        .clk(clk),
        .reset(reset),
        .address(address),
        .data_in(data_in),
        .data_out(data_out),
        .mem_read(mem_read),
        .mem_write(mem_write)
    );

    // Memory (RAM)
    Memory ram (
        .clk(clk),
        .address(address),
        .data_in(data_out),
        .data_out(data_in),
        .read(mem_read),
        .write(mem_write)
    );

    // I/O device (like a display or port)
    IODevice io (
        .clk(clk),
        .address(address),
        .data_in(data_out),
        .data_out(io_out),
        .write(mem_write)
    );

endmodule
// Simple RAM model in Verilog
module SimpleRAM (
    input clk,
    input we,                // write enable
    input [7:0] addr,        // 8-bit address (256 locations)
    input [7:0] data_in,     // data to write
    output reg [7:0] data_out // data read
);

    reg [7:0] memory [0:255]; // 256 x 8-bit memory cells

    always @(posedge clk) begin
        if (we) begin
            memory[addr] <= data_in;   // write operation
        end
        data_out <= memory[addr];      // read operation
    end
endmodule
// Simple SSD model (toy example, not real firmware)
module SimpleSSD (
    input clk,
    input we,                  // write enable
    input [31:0] addr,         // 32-bit address space
    input [7:0] data_in,       // data to write
    output reg [7:0] data_out  // data read
);

    // Pretend this is 120 GB by scaling down to a small array
    // (real SSDs use NAND flash, wear leveling, error correction, etc.)
    reg [7:0] storage [0:1023]; // tiny simulated storage (1 KB)

    always @(posedge clk) begin
        if (we) begin
            storage[addr % 1024] <= data_in; // write operation
        end
        data_out <= storage[addr % 1024];    // read operation
    end
endmodule
// Simple SSD model (toy example, not real firmware)
module SimpleSSD (
    input clk,
    input we,                  // write enable
    input [31:0] addr,         // 32-bit address space
    input [7:0] data_in,       // data to write
    output reg [7:0] data_out  // data read
);

    // Pretend this is 120 GB by scaling down to a small array
    // (real SSDs use NAND flash, wear leveling, error correction, etc.)
    reg [7:0] storage [0:1023]; // tiny simulated storage (1 KB)

    always @(posedge clk) begin
        if (we) begin
            storage[addr % 1024] <= data_in; // write operation
        end
        data_out <= storage[addr % 1024];    // read operation
    end
endmodule
// Example: Activity lifecycle method in Android
@Override
protected void onStart() {
    super.onStart();
    Log.d("MyActivity", "Activity started!");
}
// mini_os.c
// A tiny toy operating system kernel

void kernel_main(void) {
    const char *msg = "Hello from Mini OS!";
    char *video_memory = (char*)0xb8000; // VGA text buffer address

    for (int i = 0; msg[i] != '\0'; i++) {
        video_memory[i * 2] = msg[i];     // character
        video_memory[i * 2 + 1] = 0x07;   // attribute (white on black)
    }

    // Halt CPU (infinite loop)
    for (;;) {}
}
; bootloader.asm
; A simple bootloader that loads our kernel

BITS 16
ORG 0x7C00

start:
    ; Set up stack
    xor ax, ax
    mov ss, ax
    mov sp, 0x7C00

    ; Load kernel (assumes kernel is right after bootloader)
    mov si, msg
    call print_string

    jmp 0x0000:0x7E00   ; Jump to kernel entry

print_string:
    mov ah, 0x0E
.next_char:
    lodsb
    cmp al, 0
    je .done
    int 0x10
    jmp .next_char
.done:
    ret

msg db "Booting Mini OS...",0

times 510-($-$$) db 0
dw 0xAA55
// kernel.c
// A simple kernel that prints and reads keyboard input

void kernel_main(void) {
    char *video = (char*)0xb8000;
    const char *msg = "Welcome to Mini OS!";
    int i = 0;

    // Print message
    while (msg[i]) {
        video[i*2] = msg[i];
        video[i*2+1] = 0x07;
        i++;
    }

    // Wait for keyboard input (simplified)
    unsigned char scancode;
    while (1) {
        asm volatile("inb $0x60, %0" : "=a"(scancode));
        video[160] = 'K';  // Just show 'K' when a key is pressed
        video[161] = 0x0A;
    }
}
nasm -f bin bootloader.asm -o bootloader.bin
i686-elf-gcc -ffreestanding -c kernel.c -o kernel.o
qemu-system-i386 -drive format=raw,file=os.img
mini-os/
├── bootloader.asm
├── kernel.c
├── screen.c
├── screen.h
├── keyboard.c
├── keyboard.h
├── shell.c
├── shell.h
└── Makefile
BITS 16
ORG 0x7C00

start:
    mov si, msg
    call print_string

    jmp 0x0000:0x7E00   ; jump to kernel

print_string:
    mov ah, 0x0E
.next_char:
    lodsb
    cmp al, 0
    je .done
    int 0x10
    jmp .next_char
.done:
    ret

msg db "Booting Mini OS...",0

times 510-($-$$) db 0
dw 0xAA55
#include "screen.h"
#include "keyboard.h"
#include "shell.h"

void kernel_main(void) {
    clear_screen();
    print("Welcome to Mini OS!\n");
    print("Type something below:\n");

    while (1) {
        char input = get_key();
        shell_handle(input);
    }
}
// screen.h
void clear_screen();
void print(const char *str);

// screen.c
char *video = (char*)0xb8000;

void clear_screen() {
    for (int i = 0; i < 80*25; i++) {
        video[i*2] = ' ';
        video[i*2+1] = 0x07;
    }
}

void print(const char *str) {
    static int pos = 0;
    while (*str) {
        video[pos*2] = *str++;
        video[pos*2+1] = 0x07;
        pos++;
    }
}
// keyboard.h
char get_key();

// keyboard.c
char get_key() {
    unsigned char scancode;
    asm volatile("inb $0x60, %0" : "=a"(scancode));
    return scancode; // raw scancode for now
}
// shell.h
void shell_handle(char input);

// shell.c
#include "screen.h"

void shell_handle(char input) {
    if (input == 0x1C) { // Enter key scancode
        print("\nYou pressed Enter!\n");
    } else {
        print("Key pressed!\n");
    }
}
#include "screen.h"
#include "keyboard.h"

static char buffer[128];
static int buf_pos = 0;

void shell_handle(char input) {
    // Convert scancode to ASCII (simplified, only letters)
    char c = scancode_to_ascii(input);
    if (c) {
        if (c == '\n') { // Enter key
            buffer[buf_pos] = '\0';
            if (strcmp(buffer, "hello") == 0) {
                print("\nMini OS says: Hello!\n");
            } else if (strcmp(buffer, "clear") == 0) {
                clear_screen();
            } else {
                print("\nUnknown command\n");
            }
            buf_pos = 0;
        } else {
            buffer[buf_pos++] = c;
            char str[2] = {c, '\0'};
            print(str); // echo typed character
        }
    }
}
F###/
├── src/
│   ├── App.js
│   ├── components/
│   │   └── Home.js
│   └── styles.css
├── package.json
import React from "react";
import Home from "./components/Home";
import "./styles.css";

function App() {
  return (
    <div className="App">
      <h1>Welcome to F###</h1>
      <Home />
    </div>
  );
}

export default App;
import React, { useState } from "react";

function Home() {
  const [message, setMessage] = useState("");

  const handleClick = () => {
    setMessage("Hello from F### app!");
  };

  return (
    <div>
      <p>This is the home screen of F###.</p>
      <button onClick={handleClick}>Say Hello</button>
      <p>{message}</p>
    </div>
  );
}

export default Home;
.App {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}

button {
  padding: 10px 20px;
  margin-top: 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
import random

def number_guessing_game():
    print("🎮 Welcome to the Number Guessing Game!")
    number_to_guess = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("Enter your guess (1-100): "))
        attempts += 1

        if guess < number_to_guess:
            print("Too low! Try again.")
        elif guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print(f"🎉 Congratulations! You guessed it in {attempts} attempts.")
            break

number_guessing_game()
class SimpleCPU:
    def __init__(self):
        self.registers = {"A": 0, "B": 0}   # two registers
        self.memory = [0] * 16              # small memory (16 cells)
        self.pc = 0                         # program counter

    def load_program(self, program):
        self.memory[:len(program)] = program

    def run(self):
        while self.pc < len(self.memory):
            instr = self.memory[self.pc]
            self.pc += 1

            if instr[0] == "LOAD":
                self.registers[instr[1]] = instr[2]
            elif instr[0] == "ADD":
                self.registers[instr[1]] += self.registers[instr[2]]
            elif instr[0] == "STORE":
                self.memory[instr[2]] = self.registers[instr[1]]
            elif instr[0] == "HALT":
                break

# Example program
program = [
    ("LOAD", "A", 5),     # Load 5 into register A
    ("LOAD", "B", 10),    # Load 10 into register B
    ("ADD", "A", "B"),    # A = A + B
    ("STORE", "A", 0),    # Store result into memory[0]
    ("HALT",)
]

cpu = SimpleCPU()
cpu.load_program(program)
cpu.run()

print("Registers:", cpu.registers)
print("Memory:", cpu.memory)
import tkinter as tk
import time

root = tk.Tk()
root.title("Boot Animation")
root.geometry("500x300")
root.configure(bg="black")

label = tk.Label(
    root,
    text="",
    font=("Arial", 24),
    fg="lime",
    bg="black"
)
label.pack(expand=True)

boot_text = [
    "Initializing System...",
    "Loading Drivers...",
    "Starting Services...",
    "Boot Complete!"
]

def animate(index=0):
    if index < len(boot_text):
        label.config(text=boot_text[index])
        root.after(1000, animate, index + 1)

animate()
root.mainloop()
class USBDevice:
    def __init__(self, name):
        self.name = name

    def send_data(self, data):
        print(f"{self.name} sending: {data}")

    def receive_data(self, data):
        print(f"{self.name} received: {data}")

# Example
keyboard = USBDevice("USB Keyboard")
keyboard.send_data("Key Press: A")
keyboard.receive_data("Acknowledged")
class VGA:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def draw_pixel(self, x, y, char="*"):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char

    def render(self):
        for row in self.buffer:
            print("".join(row))

# Example
vga = VGA(10, 5)
vga.draw_pixel(4, 2, "#")
vga.render()
class HDMI:
    def __init__(self):
        self.video_stream = []
        self.audio_stream = []

    def send_video(self, frame):
        self.video_stream.append(frame)
        print(f"Video frame sent: {frame}")

    def send_audio(self, sample):
        self.audio_stream.append(sample)
        print(f"Audio sample sent: {sample}")

# Example
hdmi = HDMI()
hdmi.send_video("Frame 1: [###]")
hdmi.send_audio("Audio: Beep")
class TinyProcessor:
    def __init__(self):
        self.accumulator = 0
        self.memory = [0] * 256
        self.pc = 0
        self.running = True

    def execute(self, program):
        self.pc = 0
        self.running = True

        while self.running and self.pc < len(program):
            instruction = program[self.pc]
            opcode = instruction[0]

            if opcode == "LOAD":
                self.accumulator = instruction[1]

            elif opcode == "ADD":
                self.accumulator += instruction[1]

            elif opcode == "SUB":
                self.accumulator -= instruction[1]

            elif opcode == "STORE":
                address = instruction[1]
                self.memory[address] = self.accumulator

            elif opcode == "READ":
                address = instruction[1]
                self.accumulator = self.memory[address]

            elif opcode == "JMP":
                self.pc = instruction[1]
                continue

            elif opcode == "PRINT":
                print("ACC =", self.accumulator)

            elif opcode == "HALT":
                self.running = False

            else:
                raise ValueError(f"Unknown instruction: {opcode}")

            self.pc += 1


# Example program
program = [
    ("LOAD", 10),
    ("ADD", 5),
    ("STORE", 0),
    ("SUB", 3),
    ("PRINT",),
    ("READ", 0),
    ("PRINT",),
    ("HALT",)
]

cpu = TinyProcessor()
cpu.execute(program)
ACC = 12
ACC = 15
class TinyProcessor:
    def __init__(self):
        self.accumulator = 0
        self.memory = [0] * 256
        self.pc = 0
        self.running = True

    def execute(self, program):
        self.pc = 0
        self.running = True

        while self.running and self.pc < len(program):
            instruction = program[self.pc]
            opcode = instruction[0]

            if opcode == "LOAD":
                self.accumulator = instruction[1]

            elif opcode == "ADD":
                self.accumulator += instruction[1]

            elif opcode == "SUB":
                self.accumulator -= instruction[1]

            elif opcode == "HALT":
                self.running = False

            self.pc += 1


program = [
    ("LOAD", 10),
    ("ADD", 5),
    ("SUB", 3),
    ("HALT",)
]

cpu = TinyProcessor()
cpu.execute(program)

print("Final ACC value =", cpu.accumulator)Final ACC value = 12

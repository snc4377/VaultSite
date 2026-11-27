---
title: "Objeto"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "Conceptos", "objeto"]
---

# Object

### 1. What is it?

It is a **container**. Imagine a box with labels on the outside (its data) and buttons on the inside (its actions). It is a representation of something concrete (a user, an invoice, a car, an enemy in a game) within the computer's memory.

### 2. What does it do?

An object primarily does three things:

- **Stores its own information:** It doesn’t need other parts of the program to tell it what it is; it maintains its own data (e.g., "my name is Juan" and "I am 25 years old").
    
- **Performs tasks:** It can execute actions on its own data (e.g., the "User" object can perform the task of "changing password").
    
- **Communicates:** It can request things from other objects or respond when another object asks it something.
    

### 3. What is it for? (The real utility)

It serves to **organize chaos**.

- **To avoid code repetition:** If you have 100 users in your program, you don’t create 100 loose lists of data. You create a single "mold" of an object and generate 100 copies that know how to behave the same way.
    
- **To protect data:** It prevents one part of the program from accidentally breaking something in another part. Only the object can modify its own data through its "buttons" (methods).
    
- **To model reality:** It’s much easier to program by thinking in terms of "Objects interacting" than in thousands of lines of abstract mathematical instructions.
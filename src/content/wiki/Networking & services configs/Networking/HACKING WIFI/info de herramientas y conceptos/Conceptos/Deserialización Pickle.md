---
title: "Deserialización Pickle"
category: ["Networking & services configs", "Networking", "HACKING WIFI", "info de herramientas y conceptos", "Conceptos", "Deserialización Pickle"]
---

# Pickle Deserialization

## What is Pickle in Python?

Pickle is a module available in Python's standard library that allows transforming objects into byte sequences, which we can later reconstruct into in-memory objects.

The process of creating binary files from objects and data structures is called "serialization," and the reverse process is called "deserialization." These processes are used to save states in storage systems or exchange data and are frequently used to maintain persistence between executions without having to write additional code to convert structures to text or JSON.

## Why Use Pickle in Python?

As a serialization system, Pickle provides us with some important functionalities that we will describe.

### State Storage

Pickle allows saving the state of a program so that we can resume the application's execution later while retaining all the data it had at the moment it was stopped.

### Data Exchange Between Processes

It can also be used to exchange data between processes within a computer, for example, when multiple processes run concurrently on the system.

### Data Persistence Between Sessions

Serialization is also used to store data on disk, achieving persistence between sessions within the same software. This allows us to save serialized objects in a storage system, such as the computer's hard drive, so we can retrieve them even days later and after restarting the system.

### Simplifies Storage of Custom Data Structures

Serialization is a common process built into Python's standard library, as well as other programming languages having their own mechanisms. This allows applications to store state in a straightforward way without complicating developers' lives by creating custom saving mechanisms.

### Facilitates Data Transfer Between Python Scripts

Once an object is serialized, it is possible to perform any type of operation with it. This can be used potentially for many functionalities, such as transferring data between programs developed in Python.

### Part of Python's Standard Library

Thanks to Pickle, we do not need to add external dependencies to applications, as we simply use the language's standard library, available anywhere Python is used.

## How Does Serialization Work with Pickle?

Now, let's see what you need to do to serialize objects using Pickle in Python.

### dump() and load() Methods

First, let's look at the `dump()` and `load()` methods, which are the most essential for using Pickle.

- `pickle.dump(obj, file)` is used to serialize an object. This method saves the serialized object directly to a file.
- `pickle.load(file)` does the opposite: it takes the content of a file and deserializes it, returning a restored object.

### Binary and Text Formats

Unlike other formats, Pickle stores data in a binary file, enabling more powerful storage capabilities. For example, a binary file can store more information about objects, such as methods that do not have an easy representation in text. It is also faster than text storage and takes up less space.

However, if necessary, Python could also serialize to a text file, though this is not very common as it does not offer a significant advantage. The serialization format produced is specific to Python, so it cannot be used as a means of exchange in applications written in other languages.

### Types of Objects Supported by Pickle

Pickle is very versatile regarding the types of objects it supports, although it cannot serialize every type of object. It supports lists, dictionaries, tuples, sets, numbers, strings, functions, and even objects of custom classes created through common development.

However, it is important to know that not all objects are serializable with Pickle. For example, it cannot serialize open file descriptors or network connections.

For an object to be serializable, it must be an object of a class defined in a top-level module. You could not, for example, serialize a class defined inside a lambda function, as Python needs to know the class during deserialization.

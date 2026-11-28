---
title: "Redeemer"
category: ["Redeemer"]
---

- We run nmap with `-p- --min-rate 5000 -sV` to identify ports and their protocols quickly
	- Port 6379 with Redis protocol (a NoSQL data store)
	- Using `redis-cli --help` we gather information
	- Then we access via `redis-cli -h ip`
	- Running `info` shows general information, while `info keyspace` reveals how many keys exist in a specific database (previously selected with `select database_name`)
	- `keys *` displays all available keys
	- Using `get key_name` retrieves the specific key value
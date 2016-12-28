A collection of random, useful scripts that I use in various places.

Most of these scripts are primarily targeted towards Arch Linux systems, which
means some of the shebangs may not be suitable for all systems. There shouldn't
be anything preventing their use on other distributions though.

Unless otherwise stated, all code within this repository is released into the
public domain without any warranty.

Below is a list of scripts contained within this repository (in alphabetical
order).

ansible-task

This script runs a "task" playbook. This typically won't be a playbook that
puts the system into a known state but rather something that performs a task
such as mail sync.

base64_url

This script makes it easier to base64 encode and decode URL encoded values.

blockip

This adds a basic rule to iptables that drops all incoming traffic from a
particular IP address.

find-replace

This implements a basic find+replace for the terminal. I've found that ~80% of
the time when people think they want to use sed, they actually want to use
their editor's find+replace functionality. This script provides that.
TODO: Add usage note
TODO: Think about rewriting in python

ssh_key_add

This script provides a wrapper for adding named SSH keys to your SSH agent.
I deliberately named the script with underscores to make it easier to
tab-complete.

systemctl_stop_machine.py

This script is designed to gracefully stop nspawn containers that run their
own init processes that are not systemd (such as runit or s6-overlay). The
naive approach to this problem is to have an ExecStop= line in your service
unit that calls 'machinectl kill machine --kill-who=leader'. Unfortunately,
this doesn't wait for the process to terminate. Instead, it exits immediately,
and systemd then thinks the main process has not terminated and kills all
the processes within the container immediately. This script runs the above
machinectl command, then actually waits for the process to terminate before
exiting.

toggle_service

This script simply toggles a service and tells you whether or not it was
successful. It does not use sudo - instead, it assumes you have polkit
configured correctly.

woodo

It's a weird tree.

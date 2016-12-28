#!/usr/bin/python3

import argparse
import executor
from humanfriendly import Timer
import parse
import proc.unix
import sys
import time
from typing import Tuple


# TODO: Remove this override once this PR is accepted: https://github.com/xolox/python-executor/pull/3
class UnixProcess(proc.unix.UnixProcess):
    def wait_for_process(self, timeout=0, use_spinner=False):
        if use_spinner:
            return super().wait_for_process(timeout=timeout)
        timer = Timer()
        while self.is_running:
            if timeout and timer.elapsed_time >= timeout:
                break
            time.sleep(0.2)
        return timer


class NspawnMachineStopper(object):
    def __init__(self, machine):
        self._machine = machine
        self._pid = self._find_pid(machine)

    def _find_pid(self, machine: str) -> int:
        cmd = executor.ExternalCommand("machinectl show {0}".format(machine), capture=True, check=False)
        executor.execute_prepared(cmd)
        if not cmd.succeeded:
            raise MachineNotExistsException("Machine '{0}' does not exist".format(machine))

        results = parse.search("Leader={:d}", cmd.stdout.decode("utf-8"))
        try:
            pid = int(results[0])
        except (ValueError, KeyError):
            return MachineNotExistsException("Could not find PID for machine '{0}'".format(machine))
        return pid

    def stop_machine(self, timeout: int=60) -> Tuple[bool, Timer]:
        process = UnixProcess(pid=self._pid)

        stop_cmd = executor.ExternalCommand("machinectl kill {0} --kill-who=leader".format(self._machine), check=False)
        executor.execute_prepared(stop_cmd)

        timer = process.wait_for_process(timeout=timeout, use_spinner=False)
        return (process.is_running, timer)


class MachineNotExistsException(Exception):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("machine", help="The name of the nspawn machine to gracefully terminate")
    parser.add_argument("-v", "--verbose", help="Turn on verbose output", action="store_true")
    parser.add_argument("-t", "--timeout", help="The amount of time to wait for the machine to shut down", type=int, default=60)
    args = parser.parse_args()

    try:
        stopper = NspawnMachineStopper(args.machine)
    except MachineNotExistsException:
        if args.verbose:
            print("Machine '{0}' not running".format(args.machine))
        return

    is_running, timer = stopper.stop_machine(timeout=args.timeout)
    if args.verbose:
        if is_running:
            print("Failed to stop machine '{0}' after {1}".format(args.machine, timer), file=sys.stderr)
        else:
            print("Stopped machine '{0}' after {1}".format(args.machine, timer))


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print("{0}: {1}".format(e.__class__.__name__, e), file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

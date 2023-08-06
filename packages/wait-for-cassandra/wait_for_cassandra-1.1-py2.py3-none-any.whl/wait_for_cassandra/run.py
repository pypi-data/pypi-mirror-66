# coding=UTF-8
from __future__ import print_function

import time
import cassandra.cluster
import sys


def wait_for_cassandra(host_name, wait_timeout):
    start_at = time.time()
    wait_println_counter = 0
    while time.time() - start_at < wait_timeout:
        try:
            cluster = cassandra.cluster.Cluster([host_name],
                                                load_balancing_policy=
                                                cassandra.cluster.TokenAwarePolicy(
                                                    cassandra.cluster.DCAwareRoundRobinPolicy(
                                                        local_dc='datacenter1'
                                                    )
                                                ),
                                                )
            cluster.connect()

        except (cassandra.cluster.NoHostAvailable, cassandra.UnresolvableContactPoints):
            wait_println_counter += 3
            if wait_println_counter == 3:
                print("Waiting 30 more seconds...")
                wait_println_counter = 0
            time.sleep(10)
        else:
            sys.exit(0)
    else:
        print("Waiting time exceeded, aborting...")
        sys.exit(1)


def run():
    if '-h' in sys.argv:
        print('''Use like:

    wait_for_cassandra <hostname> <wait timeout>

    Default hostname is localhost, and default timeout is 300 seconds''')
        sys.exit(0)

    try:
        _, hostname, timeout = sys.argv
        timeout = int(timeout)
    except ValueError:
        try:
            _, hostname = sys.argv
            timeout = 300
        except ValueError:
            hostname = 'localhost'
            timeout = 300

    wait_for_cassandra(hostname, timeout)


if __name__ == '__main__':
    run()

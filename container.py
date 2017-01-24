#!/usr/bin/env python

import docker
import argparse
from json import dumps

from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import tzutc

parser = argparse.ArgumentParser()
parser.add_argument("--unit", type=str,
    choices=['second', 'minute', 'hour', 'day'], default='second',
    help="unit to be used in --created and --exited opt")
parser.add_argument("--created", type=long,
    help="show created containers with minimum seconds since created")
parser.add_argument("--exited", type=long,
    help="show exited containers with minimum seconds since finish")
args = parser.parse_args()

client = docker.from_env()
now = datetime.utcnow().replace(tzinfo=tzutc())
def created_seconds(container):
    time_created = parse(container.attrs['Created'])
    return long((now - time_created).total_seconds())

def exited_seconds(container):
    time_exited = parse(container.attrs['State']['FinishedAt'])
    return long((now - time_exited).total_seconds())


cons = client.containers.list(all=True)
cons = filter(lambda x: x.status in ['created', 'exited'], cons)
result = []

multiplier = 1
if args.unit == 'minute':
    multiplier = 60
elif args.unit == 'hour':
    multiplier = 60 * 60
elif args.unit == 'day':
    multiplier = 60 * 60 * 24
else:
    multiplier = 1

if args.created:
    result += filter(lambda c: created_seconds(c) >= args.created * multiplier, cons)

if args.exited:
    result += filter(lambda c: exited_seconds(c) >= args.exited * multiplier, cons)

for c in result:
    print c.id

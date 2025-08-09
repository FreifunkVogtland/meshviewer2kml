#!/usr/bin/python3
# -*- coding: utf-8; -*-
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2017-2020, Sven Eckelmann <sven@narfation.org>

import copy
from datetime import datetime
from fastkml import kml
from fastkml.data import ExtendedData, Data
import json
import os
import os.path
import sys
from shapely.geometry import Point


def dump_kml(data, filename):
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write(data.to_string())
        f.flush()
        os.fsync(f.fileno())


def generate_kml(meshviewer):
    k = kml.KML()
    d = kml.Document()
    k.append(d)

    for n in meshviewer['nodes']:
        if 'location' not in n:
            continue

        if 'latitude' not in n['location']:
            continue

        if 'longitude' not in n['location']:
            continue

        if 'hostname' not in n:
            continue

        if 'node_id' not in n:
            continue

        if 'is_online' not in n:
            continue

        extended = ExtendedData()

        point = Point(n['location']['longitude'], n['location']['latitude'])
        p = kml.Placemark(id=n['node_id'], name=n['hostname'], geometry=point)
        d.append(p)

        extended = []

        if n['is_online']:
            status = "online"
        else:
            status = "offline"

        extended.append(Data(value=status, name='status', display_name='Status'))

        url = 'https://vogtland.freifunk.net/map/#!/map/'+n['node_id']
        extended.append(Data(value=url, name='url', display_name='URL'))

        p.extended_data = ExtendedData(elements=extended)


    return k


def main():
    if len(sys.argv) != 3:
        print("./nodes2kml.py MESHVIEWERJSON OUTKML")
        sys.exit(1)

    meshviewerjson = sys.argv[1]
    outkml = sys.argv[2]
    outkmltmp = outkml + '.tmp'

    # load
    meshviewer = json.load(open(meshviewerjson))
    data = generate_kml(meshviewer)

    # store
    dump_kml(data, outkmltmp)
    os.rename(outkmltmp, outkml)


if __name__ == "__main__":
    main()

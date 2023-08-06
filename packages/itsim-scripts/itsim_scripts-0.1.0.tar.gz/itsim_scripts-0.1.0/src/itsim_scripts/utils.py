from argparse import Namespace
from gtfstk.feed import read_gtfs, write_gtfs
from json import dumps, loads
from math import ceil
from os import makedirs
from os.path import basename, dirname, exists, join, splitext
from pathlib import Path
from shapefile import Reader
from shutil import copyfile
from unicodedata import normalize, category


layer_types = [
    'surfaces_density',  # front will ask for computation on surfaces
    'dots_value',  # front will ask for computation on points
    'lines_and_dots',  # front will not ask for computation
]


def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean filename.
    Remove leading and trailing spaces;
    convert other spaces to underscores;
    and remove anything that is not an alphanumeric, dash, underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    NFKD = Normal Format with Kompatibility using Decomposition of characters
    See https://www.unicode.org/reports/tr44/tr44-6.html#General_Category_Values
    """
    return ''.join([
        c for c in normalize('NFKD', s.strip())
        if category(c) in ('Lu', 'Ll', 'Nd', 'Zs') or c in ('_', '.', '-')
    ]).replace(' ', '_').strip('_.-').lower()


def get_geometry(shape):
    # this is super private but the implementation is open and trivial
    # if this property disappears, code could simply be copied.
    return shape.__geo_interface__


def _decode_value(value):
    if callable(getattr(value, 'decode', None)):
        try:
            value = value.decode('utf8')
        except UnicodeDecodeError:
            try:
                value = value.decode('latin1')
            except UnicodeDecodeError:
                value = value.decode('ascii', errors='ignore')
    return value


def get_geojson(shape_file, field_from=None, field_to=None):
    sf = Reader(shape_file)
    try:
        shape_records = sf.shapeRecords()
    except UnicodeDecodeError:
        sf = Reader(shape_file, encoding='latin1', encodingErrors='replace')
        shape_records = sf.shapeRecords()
    field_names = [field[0] for field in sf.fields if not field[0].startswith("Deletion")]
    features = []
    id = 1
    if field_from and field_to:
        def filter_attrs(zip_in):
            return {field_to: v for k, v in zip_in if k == field_from}
    else:
        def filter_attrs(zip_in):
            return dict(zip_in)
    for shape_record in shape_records:
        geometry = get_geometry(shape_record.shape)
        attrs = filter_attrs(zip(field_names, shape_record.record))
        for attr, value in attrs.items():
            attrs[attr] = _decode_value(value)
        value = attrs.get(field_to or field_from, None)
        if value is None or type(value) not in (int, float) or value > 0:
            for id_name in ('id', 'ID', 'Id', 'iD'):
                if id_name in attrs:
                    attrs['originid'] = attrs[id_name]
                    del attrs[id_name]
            feature = {
                'type': 'Feature',
                'id': id,
                'geometry': geometry,
                'properties': attrs,
            }
            id += 1
            features.append(feature)
    return {
        'type': 'FeatureCollection',
        'features': features,
    }


def _field_type_to_str(field_type, field_decimal_len):
    if field_type in ('N', 'F'):
        if field_decimal_len:
            return "float"
        else:
            return "int"
    elif field_type == 'D':
        return "date"
    elif field_type == 'L':
        return "bool"
    else:
        return "varchar"


def _find_intervals(values, num, exclude_zero):
    if exclude_zero:
        values = [v for v in values if v and v > 0]
    else:
        values = values[:]
    values.sort()
    intervals = []
    idx = 0
    size = len(values)
    for i in range(num):
        if idx >= size:
            continue
        idx_from = idx
        idx += (len(values) - sum(map(len, intervals))) // (num - i)
        part = values[idx_from:idx]
        max_value = part[-1]
        max_count_in_part = part.count(max_value)
        max_count_other = values[idx:].count(max_value)
        if max_count_other:
            if max_count_other > max_count_in_part \
                    and idx - max_count_in_part > idx_from \
                    and values[idx_from] != values[idx - max_count_in_part]:
                idx -= max_count_in_part
            else:
                idx += max_count_other
            part = values[idx_from:idx]
        intervals.append(part)
    return intervals


def get_first_record_attributes(shape_file, field_from=None, num=5, min_color='FEE5D9', max_color='A50F15'):
    info = {
        'records_size': 0,
        'fields': [],
        'legend': [],
        'legend_as_param': '',
    }
    sf = Reader(shape_file)
    try:
        records = sf.records()
    except UnicodeDecodeError:
        sf = Reader(shape_file, encoding='latin1', encodingErrors='replace')
        records = sf.records()
    fields = [field for field in sf.fields if not field[0].startswith("Deletion")]
    info['records_size'] = len(records)
    record = records[0]
    for field, value in zip(fields, record):
        info['fields'].append({
            'name': field[0],
            'type': _field_type_to_str(field[1], field[3]),
            'one_value': _decode_value(value),
        })
    if field_from:
        values = []
        for record in sf.records():
            for field, value in zip(fields, record):
                if field[0] == field_from:
                    values.append(_decode_value(value))
        intervals = _find_intervals(values, num, True)
        RED = 0
        GREEN = 1
        BLUE = 2
        delta_red = (max_color[RED] - min_color[RED]) / (num - 1)
        delta_green = (max_color[GREEN] - min_color[GREEN]) / (num - 1)
        delta_blue = (max_color[BLUE] - min_color[BLUE]) / (num - 1)
        legend_as_param = []
        for i, interval in enumerate(intervals):
            legend_part = {
                'max_value': ceil(interval[-1]),
                'nb_values': len(interval),
                'percent': round(len(interval) / len(values) * 100, 2),
                'color': "#{:02X}{:02X}{:02X}".format(
                    int(min_color[RED] + i * delta_red),
                    int(min_color[GREEN] + i * delta_green),
                    int(min_color[BLUE] + i * delta_blue)
                )
            }
            info['legend'].append(legend_part)
            legend_as_param.append('{},{}'.format(legend_part['max_value'], legend_part['color'][1:]))
        info['legend_as_param'] = ','.join(legend_as_param)
    return info


def filter_gtfs(gtfs_file, route_ids_file, in_file, out_file):
    with open(route_ids_file) as f:
        route_ids = [v for v in f.read().strip().split('\n')]
    feed = read_gtfs(gtfs_file, 'm')
    feed_in = feed.restrict_to_routes([id for id in feed.routes['route_id'] if id in route_ids])
    makedirs(dirname(in_file), exist_ok=True)
    write_gtfs(feed_in, in_file)
    feed_out = feed.restrict_to_routes([id for id in feed.routes['route_id'] if id not in route_ids])
    makedirs(dirname(out_file), exist_ok=True)
    write_gtfs(feed_out, out_file)


def export_gtfs_to_geojson(gtfs_file, json_file):
    feed = read_gtfs(gtfs_file, 'm')
    feed = feed.create_shapes()
    features = []
    for route_id in feed.routes['route_id']:
        features.extend(feed.route_to_geojson(route_id, include_stops=True)['features'])
    geojson = {
        'type': 'FeatureCollection',
        'features': features,
    }
    makedirs(dirname(json_file), exist_ok=True)
    with open(json_file, "w") as f:
        f.write(dumps(geojson, ensure_ascii=False))


def _get_project_scenarios(scenarios):
    it = iter(scenarios)
    try:
        while True:
            name, routes, one_pattern_per_route = next(it)
            if routes.lower() == 'all':
                routes = 'all'
            elif routes.lower() == 'none':
                routes = 'None'
            else:
                routes = routes.split(',')
            yield {
                'name': name,
                'routes': routes,
                'keep_only_one_pattern_per_route': str(one_pattern_per_route in ('true', 'True', '1')),
            }
    except StopIteration:
        return


def _get_project_buffer_size_default(buffers):
    return {'inherit': str(True), 'value': buffers[-1]} if len(buffers) else {}


def _get_project_buffer_size_by_mode(buffers):
    if len(buffers) % 2 == 1:
        buffers = buffers[:-1]
    if len(buffers) < 2:
        return
    else:
        it = iter(buffers)
        try:
            while True:
                mode, value = next(it), next(it)
                yield str(mode), value
        except StopIteration:
            return


def _get_project_cost_per_kilometer_default(costs):
    return {'inherit': str(True), 'value': costs[-1]} if len(costs) else {}


def _get_project_cost_per_kilometer_by_mode(costs):
    if len(costs) % 2 == 1:
        costs = costs[:-1]
    if len(costs) < 2:
        return
    else:
        it = iter(costs)
        try:
            while True:
                mode, value = next(it), next(it)
                yield str(int(mode)), value
        except StopIteration:
            return


def _get_project_typical_days(typical_days):
    if len(typical_days) < 2:
        return
    else:
        it = iter(typical_days)
        try:
            while True:
                name, date = next(it), next(it)
                yield {
                    'name': name,
                    'ref_scenario_date': int(date),
                    'proj_scenario_date': int(date),
                }
        except StopIteration:
            return


def _get_project_time_types(time_types):
    if len(time_types) < 3:
        return
    else:
        it = iter(time_types)
        id = 1
        try:
            while True:
                name, start_time, end_time = next(it), next(it), next(it)
                yield {
                    'id': id,
                    'name': name,
                    'type': 'time_type',
                    'startTime': start_time,
                    'endTime': end_time,
                }
                id += 1
        except StopIteration:
            return


def _get_project_legend_filters(legend, prop):
    if ',' in legend:
        it = iter(legend.split(','))
        min_value = 0
        try:
            while True:
                max_value, color = int(next(it)), next(it)
                yield {
                    'property': prop,
                    'minValue': min_value,
                    'maxValue': max_value,
                    'fillColor': '#{}'.format(color),
                }
                min_value = max_value
        except StopIteration:
            return
    else:
        color = legend
        yield {
            'property': prop,
            'fillColor': '#{}'.format(color),
        }


def _split_by_lang(value, default_i18n, prop):
    res = {}
    if value != "none":
        if value in default_i18n:
            res = default_i18n.get(value).get(prop)
        else:
            it = iter(value.split(','))
            try:
                while True:
                    lang, text = next(it, None), next(it, None)
                    if lang is None:
                        break
                    res[lang] = text
            except StopIteration:
                return
    return res


def _get_project_layer_info(layer, position):
    layer_type = layer[0]
    tileset_id = layer[1]
    tileset_name = layer[2]
    name = tileset_id.split('.')[1]  # remove mapbox username
    i18n_json_file = Path(__file__).resolve().parent / 'i18n.json'
    with open(i18n_json_file, 'r') as f:
        default_i18n = loads(f.read())
    layer_name = _split_by_lang(layer[3], default_i18n, "layer_name")
    layer_unit = _split_by_lang(layer[4], default_i18n, "layer_unit")
    layer_value_name = _split_by_lang(layer[5], default_i18n, "layer_value_name")
    layer_value_description = _split_by_lang(layer[6], default_i18n, "layer_value_description")
    layer_value_unit = _split_by_lang(layer[7], default_i18n, "layer_value_unit")
    shape_or_json_file = layer[8]
    property_from = layer[9]
    if property_from == "none":
        property_from = None
    property_to = layer[10]
    if property_to == "none":
        property_to = property_from
    legend = layer[11]
    filters = list(_get_project_legend_filters(legend, property_to)) if legend != "none" and property_to else None
    if splitext(shape_or_json_file)[1].lower() == '.json':
        shape_file = None
        shape_fields = {}
        json_file = shape_or_json_file
    else:
        shape_file = shape_or_json_file
        shape_fields = {f['name']: f['type'] for f in get_first_record_attributes(shape_file)['fields']}
        json_file = None
    data_key = "layer_{:03d}".format(position)
    return Namespace(**{
        'data_key': data_key,
        'tileset_id': tileset_id,
        'tileset_name': tileset_name,
        'name': name,
        'layer_type': layer_type,
        'layer_name': layer_name,
        'layer_unit': layer_unit,
        'layer_value_name': layer_value_name,
        'layer_value_description': layer_value_description,
        'layer_value_unit': layer_value_unit,
        'shape_file': shape_file,
        'json_file': json_file,
        'property_from': property_from,
        'property_to': property_to,
        'filters': filters,
        'fields': shape_fields,
    })


def _rename_id_field(fields):
    new_fields = {}
    for name, value in fields.items():
        if name.lower() == 'id':
            new_fields['originid'] = value
        else:
            new_fields[name] = value
    return new_fields


def get_project_json(orga_name, project_name, name_norm, desc, gtfs_file, ref_name, ref_desc, scenarios, layers, buffers, costs, turnaround_minimum, turnaround_percentage, typical_days, time_types, center, distance_unit, currency):  # noqa E501
    json = {
        'projects': {
            'org_name': orga_name,
            'project_name': project_name,
            'project_description': desc,
            'default_project_parameters': {},
            'new_scenarios': [],
        },
        'layers': {
            'list_layers': [],
        },
    }
    params = json['projects']['default_project_parameters']
    if buffers:
        if buffers[-1] != 0:
            params['buffer_size_default'] = _get_project_buffer_size_default(buffers)
        if len(buffers) > 1:
            params['buffer_size_by_mode'] = {
                'inherit': str(True),
                'value': dict(_get_project_buffer_size_by_mode(buffers)),
            }
    if costs:
        if costs[-1] != 0:
            params['cost_per_kilometer_default'] = _get_project_cost_per_kilometer_default(costs)
        if len(costs) > 1:
            params['cost_per_kilometer_by_mode'] = {
                'inherit': str(True),
                'value': dict(_get_project_cost_per_kilometer_by_mode(costs)),
            }
    if turnaround_minimum is not None:
        params['turnaround_minimum'] = {
            'inherit': str(True),
            'value': turnaround_minimum,
        }
    if turnaround_percentage is not None:
        params['turnaround_percentage'] = {
            'inherit': str(True),
            'value': turnaround_percentage,
        }
    params['typical_days'] = {
        'inherit': str(False),
        'value': list(_get_project_typical_days(typical_days)),
    }
    params['distance_unit'] = {
        'inherit': str(False),
        'value': distance_unit,
    }
    params['currency'] = {
        'inherit': str(False),
        'value': currency,
    }
    if time_types:
        params['time_type'] = {
            'inherit': str(True),
            'value': list(_get_project_time_types(time_types)),
        }
    if center:
        params['geographicalCoordinates'] = {
            'inherit': str(False),
            'value': {
                'latlng': [center[1], center[0]],
            },
        }
    if gtfs_file:
        gtfs_dest_file = join('gtfs', '{}.zip'.format(name_norm))
        if gtfs_file != gtfs_dest_file:
            makedirs(dirname(gtfs_dest_file), exist_ok=True)
            copyfile(gtfs_file, gtfs_dest_file)
        json['projects']['gtfs_name'] = name_norm
        if ref_name:
            json['projects']['reference_scenario_name'] = ref_name
            json['projects']['reference_scenario_description'] = ref_desc
        if scenarios:
            json['projects']['new_scenarios'] = list(_get_project_scenarios(scenarios))
    if layers:
        mapbox_layers = []
        list_layers = []
        for i, layer in enumerate(layers):
            layer_info = _get_project_layer_info(layer, i + 1)
            mapbox_layer = {
                'dataKey': layer_info.data_key,
                'tilesetId': layer_info.tileset_id,
                'tilesetName': layer_info.tileset_name,
                'layerType': layer_info.layer_type,
                'layerName': layer_info.layer_name,
                'layerUnit': layer_info.layer_unit,
                'layerValueName': layer_info.layer_value_name,
                'layerValueDescription': layer_info.layer_value_description,
                'layerValueUnit': layer_info.layer_value_unit,
                'isCheckboxLayer': layer_info.layer_type != 'surfaces_density',
            }
            if layer_info.property_from:
                mapbox_layer['layerTable'] = layer_info.name
                mapbox_layer['layerProperty'] = layer_info.property_from
            if layer_info.filters:
                mapbox_layer['filters'] = layer_info.filters
            mapbox_layers.append(mapbox_layer)
            if layer_info.shape_file:
                base_name = splitext(layer_info.shape_file)[0]
                dest_base_path = join('data', name_norm, basename(base_name))
                makedirs(dirname(dest_base_path), exist_ok=True)
                for ext in ('.shp', '.shx', '.dbf', '.prj'):
                    src_file = base_name + ext
                    dest_file = dest_base_path + ext
                    if exists(src_file) and src_file != dest_file:
                        copyfile(src_file, dest_file)
                geojson = get_geojson(layer_info.shape_file, layer_info.property_from, layer_info.property_to)
                dest_json_file = join('data', name_norm, layer_info.name) + '.json'
                makedirs(dirname(dest_json_file), exist_ok=True)
                with open(dest_json_file, 'w') as f:
                    f.write(dumps(geojson, ensure_ascii=False))
                    f.write('\n')
                list_layers.append({
                    'name': layer_info.name,
                    'emp': dest_base_path + '.shp',
                    'params': _rename_id_field(layer_info.fields),
                    'layerTypeDB': 'point' if layer_info.layer_type == 'dots_value' else 'polyline',
                    'layerPropertyDB': layer_info.property_from
                })
            elif layer_info.json_file:
                dest_json_file = join('data', name_norm, layer_info.name) + '.json'
                if layer_info.json_file != dest_json_file:
                    makedirs(dirname(dest_json_file), exist_ok=True)
                    copyfile(layer_info.json_file, dest_json_file)
        params['gis'] = {
            'inherit': str(True),
            'value': {
                'mapbox': {
                    'layers': mapbox_layers,
                }
            }
        }
        json['layers']['list_layers'] = list_layers
    return json

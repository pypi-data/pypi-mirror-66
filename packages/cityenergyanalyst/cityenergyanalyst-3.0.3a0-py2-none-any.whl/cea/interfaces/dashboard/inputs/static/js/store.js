class InputStore {
    constructor(store) {
        this.tables = store['tables'];
        this.geojsons = store['geojsons'];
        this.columns = store['columns'];
        this.column_types = store['column_types'];
        this.glossary = store['glossary'];
        this.crs = store['crs'];
        this.changes = {update:{},delete:{}};

        this.data = {};
        this.geojsondata = {};
        this.selected = [];

        this.generateGeojsonData();
        this.generateData();
    }

    getColumns(table) {
        return this.columns[table]
    }

    getColumnTypes(table) {
        return this.column_types[table]
    }

    getData(table) {
        return this.data[table]
    }

    getSelected() {
        return this.selected
    }

    setSelected(array) {
        this.selected = array;
    }

    getGeojson(layer) {
        return this.geojsondata[layer]
    }

    createNewGeojson(layer) {
        this.geojsondata[layer] = JSON.parse(JSON.stringify(this.geojsondata[layer]));
    }

    getGeojsonID(layer, building) {
        var features = this.geojsondata[layer]['features'];
        return features.findIndex(x => x['properties']['Name'] === building);
    }

    addChange(method, table, building, column, value) {
        var change = {[column]:value};
        if (method === 'update') {
            //Check if update is the same as default
            if (this.tables[table][building][column] === value) {
                if (this._checkNestedProp(this.changes, method, table, building, column)) {
                    delete this.changes[method][table][building][column];
                    if (!Object.keys(this.changes[method][table][building]).length) {
                        delete this.changes[method][table][building];
                    }
                }
            } else {
                this.changes[method][table] = this.changes[method][table] || {};
                this.changes[method][table][building] = this.changes[method][table][building] || {};
                Object.assign(this.changes[method][table][building], change);
            }
            console.log(this.changes);
        }
        window.parent.postMessage(true, '*');
    }

    changesToString() {
        var out = '';

        if (!$.isEmptyObject(this.changes['update'])) {
            out += '<br>UPDATED:<br>';
            $.each(this.changes['update'], function (table, buildings) {
                out += `${table}:<br>`;
                $.each(buildings, function (name, properties) {
                    out += `${name}: `;
                    $.each(properties, function (property, value) {
                        out += `${property}:${value} `;
                    });
                    out += '<br>';
                });
                out += '<br>';
            });
        }

        if (!$.isEmptyObject(this.changes['delete'])) {
            out += '<br>DELETED:<br>';
            $.each(this.changes['delete'], function (layer, buildings) {
                out += `${layer}:<br>${buildings}<br>`;
            });
            out += '<br>';
        }

        return out;
    }

    generateGeojsonData() {
        this.geojsondata = JSON.parse(JSON.stringify(this.geojsons));
    }

    generateData() {
        var _this = this;
        $.each(_this.tables, function (property, table) {
            var out = [];
            $.each(table, function (building, columns) {
                out.push({'Name': building, ...columns});
            });
            _this.data[property] = [...out];
        });
    }

    deleteBuildings(layer, buildings) {
        this.changes['delete'][layer] = this.changes['delete'][layer] || [];
        this.changes['delete'][layer].push(...buildings);
        var _this = this;
        $.each(buildings, function (_, building) {
            if (layer === 'surroundings') {
                _this.data[layer] = _this.data[layer].filter(x => x['Name'] !== building);
            } else {
                $.each(_this.data, function (table_name, table) {
                    if (table_name !== 'surroundings') {
                        _this.data[table_name] = table.filter(x => x['Name'] !== building);
                    }
                });
            }

            // Remove building from changes if being deleted
            $.each(Object.keys(_this.tables), function (_, table) {
                if (_this.changes['update'][table]) {
                    delete _this.changes['update'][table][building];
                    if (!Object.keys(_this.changes['update'][table]).length) delete _this.changes['update'][table];
                }
            });

            _this.geojsondata[layer]['features'] = _this.geojsondata[layer]['features'].filter(x => x['properties']['Name'] !== building);
        });
        this.geojsondata = JSON.parse(JSON.stringify(this.geojsondata));
    }

    resetChanges() {
        this.changes = {update:{},delete:{}};
        this.generateData();
        this.generateGeojsonData();

        window.parent.postMessage(false, '*');
    }

    applyChanges(data) {
        var _this = this;
        if (Object.keys(data['tables']).length) {
            $.each(data['tables'], function (table, columns) {
                _this.tables[table] = columns;
            })
        }

        if (Object.keys(data['geojsons']).length) {
            $.each(data['geojsons'], function (table, props) {
                console.log('props',props);
                if (Object.keys(props).length) {
                    _this.geojsons[table] = props;
                } else {
                    delete _this.geojsons[table];
                }

            })
        }

        this.resetChanges();
    }

    _checkNestedProp(obj, level,  ...rest) {
        if (obj === undefined) return false;
        if (rest.length === 0 && obj.hasOwnProperty(level)) return true;
        return this._checkNestedProp(obj[level], ...rest)
    }
}
const { DeckGL, GeoJsonLayer } = deck;
const lightMap = {
  version: 8,
  sources: {
    "osm-tiles": {
      type: "raster",
      tiles: [
        "http://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "http://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "http://b.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ],
      tileSize: 256,
      attribution: "Map data © OpenStreetMap contributors"
    }
  },
  layers: [
    {
      id: "osm-tiles",
      type: "raster",
      source: "osm-tiles",
      minzoom: 0,
      maxzoom: 22
    }
  ]
};

const darkMap = {
  version: 8,
  sources: {
    "carto-tiles": {
      type: "raster",
      tiles: [
        "https://cartodb-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
        "https://cartodb-basemaps-b.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",
        "https://cartodb-basemaps-c.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"
      ],
      tileSize: 256,
      attribution:
        "Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    }
  },
  layers: [
    {
      id: "carto-tiles",
      type: "raster",
      source: "carto-tiles",
      minzoom: 0,
      maxzoom: 22
    }
  ]
};

const jsonURLs = {
  streets: "/inputs/geojson/others/streets",
  dh: "/api/inputs/others/dh/geojson",
  dc: "/api/inputs/others/dc/geojson"
};

const defaultColors = {
  zone: [68, 76, 83],
  surroundings: [255, 255, 255],
  streets: [255, 255, 255],
  dh: [240, 75, 91],
  dc: [63, 192, 194]
};

class MapClass {
  constructor(container = "map", colors = {}) {
    this.data = {};
    this.layerProps = {};
    this.updateTriggers = {};

    this.cameraOptions = {};
    this.currentViewState = {
      latitude: 0,
      longitude: 0,
      zoom: 0,
      bearing: 0,
      pitch: 0
    };

    this.mapStyles = { light: lightMap, dark: darkMap };
    this.jsonURLs = jsonURLs;
    this.colors = { ...defaultColors, ...colors };
    this.layers = [];

    this.deckgl = new DeckGL({
      container: container,
      mapStyle: this.mapStyles.light,
      viewState: this.currentViewState,
      layers: [],
      onViewStateChange: ({ viewState }) => {
        this.currentViewState = viewState;
        this.deckgl.setProps({ viewState: this.currentViewState });
      }
      // controller: {dragRotate: false}
    });

    $(`#${container}`)
      .attr("oncontextmenu", "return false;")
      .append('<div id="map-tooltip"></div>')
      .append(
        '<div id="layers-group" style="color: black; visibility: hidden;"></div>'
      )
      .append(
        `<div id="network-group" style="position: absolute; z-index: 5; background: #fff; padding: 5px;">
          <span>Network Type:</span>
        </div>`
      );
  }

  init({ data = {}, extrude = false } = {}) {
    let _this = this;
    try {
      $.each(data, function(key, value) {
        console.log(key, value);
        value && _this.addLayer(key, value);
      });

      this.calculateCamera();

      setupButtons(this);

      this.currentViewState = {
        ...this.currentViewState,
        zoom: this.cameraOptions.zoom,
        latitude: this.cameraOptions.center.lat,
        longitude: this.cameraOptions.center.lng
      };

      this.deckgl.getMapboxMap().once("styledata", function() {
        _this.setCamera({
          transitionDuration: 300,
          onTransitionEnd: () => {
            extrude && $("#3d-button").trigger("click");
          }
        });
        $('.mapboxgl-ctrl-icon[data-toggle="tooltip"]').tooltip();
      });

      this.redraw();

      this.fetchStreets();
      this.fetchNetwork();
    } catch (e) {
      console.error("Init method requires a zone geojson\n", e);
    }
  }

  fetchStreets() {
    let _this = this;
    $.getJSON(this.jsonURLs.streets, function(json) {
      console.log("streets", json);
      if (json) {
        _this.addLayer("streets", json);
        _this.redraw();
      }
    }).fail(function() {
      console.log(`Get streets failed.`);
    });
  }

  fetchNetwork() {
    let _this = this;
    $.each(["dc", "dh"], function(_, network) {
      $(`#${network}-toggle-label`).remove();
      $(`#${network}-network-warning`).remove();
      $(`#${network}-network-error`).remove();
      $("#network-group").append(`
          <div id="${network}-network-loading">Fetching ${network.toUpperCase()} network...</div>
        `);
      $.getJSON(_this.jsonURLs[network], function(json) {
        console.log(network, json);
        $(`#${network}-network-loading`).remove();
        if (json) {
          _this.addLayer(network, json);
          _this.redraw();
        } else {
          $("#network-group").append(`
          <div id="${network}-network-warning">No ${network.toUpperCase()} network found</div>
        `);
        }
      }).fail(function() {
        $(`#${network}-network-loading`).remove();
        $("#network-group").append(`
          <div id="${network}-network-error">Error fetching ${network.toUpperCase()} network</div>
        `);
        console.log(`Get ${network} failed.`);
      });
    });
  }

  calculateCamera() {
    let bbox = this.data.zone.bbox;
    this.cameraOptions = this.deckgl
      .getMapboxMap()
      .cameraForBounds([[bbox[0], bbox[1]], [bbox[2], bbox[3]]], {
        maxZoom: 18
      });

    return bbox;
  }

  setCamera(options = {}) {
    this.deckgl.setProps({
      viewState: {
        ...this.currentViewState,
        ...options
      }
    });
  }

  setLayerProps(layer, props) {
    if (this.data.hasOwnProperty(layer)) {
      for (var prop in props) {
        if (prop !== "updateTriggers") {
          this.layerProps[layer] = {
            ...this.layerProps[layer],
            [prop]: props[prop]
          };
        } else {
          this.updateTriggers[layer] = props[prop];
        }
      }
      // this.renderLayer(layer);
    } else {
      console.error("Layer " + layer + " does not exist");
    }
  }

  addLayer(layer, data) {
    let _this = this;
    this.data = {
      ...this.data,
      [layer]: data
    };
    const layersGroup = $("#layers-group");
    const networkGroup = $("#network-group");
    switch (layer) {
      case "zone":
      case "surroundings":
      case "streets":
        !$(`#${layer}-layer-toggle`).length &&
          layersGroup.append(`
            <span class="layer-toggle" id="${layer}-layer-toggle">
              <label id='connected-label' class="map-plot-label">
                  <input id='${layer}-cb' type='checkbox' name='layer-toggle' value='${layer}' checked>
                  ${layer.charAt(0).toUpperCase() + layer.slice(1)}
              </label>
            </span>`);
        $(`#${layer}-cb`).click(_this.redraw.bind(_this));
        break;
      case "dc":
      case "dh":
        !$(`#${layer}-toggle-label`).length &&
          networkGroup.append(`
            <label class="map-plot-label network-toggle-label" id="${layer}-toggle-label" style="display: block">
              <input type="radio" id="${layer}-rd" name="network-type" value="${layer}"
              ${$(".network-toggle-label").length < 1 ? "checked" : ""}>
              ${layer === "dc" ? "District Cooling" : "District Heating"}
            </label>`);
        $(`#${layer}-rd`).click(_this.redraw.bind(_this));
        !$(`#network-layer-toggle`).length &&
          layersGroup.append(`
            <span class="layer-toggle" id="network-layer-toggle">
              <label id='connected-label' class="map-plot-label">
                  <input id='network-cb' type='checkbox' name='layer-toggle' value='network' checked>
                  Network
              </label>
            </span>`);
        $(`#network-cb`).click(_this.redraw.bind(_this));
        break;
    }
  }

  redraw() {
    let extruded =
      document.getElementById(`3d-button`).dataset.extruded === "true";
    const zoneToggle = document.getElementById(`zone-cb`);
    const surroundingsToggle = document.getElementById(`surroundings-cb`);
    const streetsToggle = document.getElementById(`streets-cb`);
    const networkToggle = document.getElementById(`network-cb`);
    const networkType = this.getNetworkType();
    const updateTriggers = this._getUpdateTriggers();
    // Add zone layer
    let layers = [
      new GeoJsonLayer({
        id: "zone",
        data: this.data.zone,
        opacity: 0.5,
        wireframe: true,
        filled: true,
        extruded: extruded,
        visible: zoneToggle.checked,

        getElevation: f => f.properties["height_ag"],
        getFillColor: this.colors.zone,
        updateTriggers: {
          getFillColor: networkType,
          ...updateTriggers.zone
        },

        pickable: true,
        autoHighlight: true,
        highlightColor: [255, 255, 0, 128],

        onHover: updateTooltip,

        ...this.layerProps.zone
      })
    ];

    if (this.data.surroundings)
      layers.push(
        new GeoJsonLayer({
          id: "surroundings",
          data: this.data.surroundings,
          opacity: 0.3,
          wireframe: true,
          filled: true,
          extruded: extruded,
          visible: surroundingsToggle.checked,

          getElevation: f => f.properties["height_ag"],
          getFillColor: this.colors.surroundings,
          updateTriggers: { ...updateTriggers.surroundings },

          pickable: true,
          autoHighlight: true,
          highlightColor: [255, 255, 0, 128],

          onHover: updateTooltip,

          ...this.layerProps.surroundings
        })
      );

    if (this.data.streets)
      layers.push(
        new GeoJsonLayer({
          id: "streets",
          data: this.data.streets,
          opacity: 0.3,
          visible: streetsToggle.checked,

          getLineColor: this.colors.streets,
          getLineWidth: 3,

          pickable: true,
          autoHighlight: true,

          onHover: updateTooltip,

          ...this.layerProps.streets
        })
      );

    // Add DC network layer
    if (this.data.dc)
      layers.push(
        new GeoJsonLayer({
          id: "dc",
          data: this.data.dc,
          stroked: false,
          filled: true,
          visible: networkType === "dc" && networkToggle.checked,

          getLineColor: this.colors.dc,
          getFillColor: f => nodeFillColor(f.properties["Type"], "dc"),
          getLineWidth: 3,
          getRadius: 3,

          pickable: true,
          autoHighlight: true,

          onHover: updateTooltip,

          ...this.layerProps.dc
        })
      );

    // Add DH network layer
    if (this.data.dh)
      layers.push(
        new GeoJsonLayer({
          id: "dh",
          data: this.data.dh,
          stroked: false,
          filled: true,
          visible: networkType === "dh" && networkToggle.checked,

          getLineColor: this.colors.dh,
          getFillColor: f => nodeFillColor(f.properties["Type"], "dh"),
          getLineWidth: 3,
          getRadius: 3,

          pickable: true,
          autoHighlight: true,

          onHover: updateTooltip,

          ...this.layerProps.dh
        })
      );

    this.deckgl.setProps({ layers });
  }

  updateData(layer, data) {
    if (Object.keys(this.data).includes(layer)) {
      this.data = {
        ...this.data,
        [layer]: data
      };
    } else {
      console.log(`Layer ${layer} does not exist`);
    }
  }

  getNetworkType() {
    const selected = document.querySelector(
      `input[name="network-type"]:checked`
    );
    if (selected) return selected.value;
    return null;
  }

  _getUpdateTriggers() {
    const out = {};
    for (var layer in this.updateTriggers) {
      out[layer] = {};
      for (var triggerProp in this.updateTriggers[layer]) {
        const trigger = this.updateTriggers[layer][triggerProp];
        if (typeof trigger === "function") out[layer][triggerProp] = trigger();
        if (Array.isArray(trigger)) {
          out[layer][triggerProp] = trigger.map(func => func());
        }
      }
    }
    return out;
  }
}

function setupButtons(MapClass) {
  const _this = MapClass;

  class dToggle {
    constructor() {
      this._extruded = false;
    }
    onAdd(map) {
      this._map = map;

      this._btn = document.createElement("button");
      this._btn.id = "3d-button";
      this._btn.className = "mapboxgl-ctrl-icon mapboxgl-ctrl-3d";
      this._btn.type = "button";
      this._btn.setAttribute("data-extruded", this._extruded);
      this._btn.setAttribute("data-toggle", "tooltip");
      this._btn.setAttribute("data-placement", "left");
      this._btn.setAttribute("data-container", "body");
      this._btn.setAttribute("data-trigger", "hover");
      this._btn.setAttribute("title", "Toggle 3D");
      this._btn.onclick = function() {
        this._extruded = !this._extruded;
        this.setAttribute("data-extruded", this._extruded);
        let pitch;
        let bearing;
        if (this._extruded) {
          pitch = 45;
        } else {
          pitch = 0;
          bearing = 0;
        }

        let className = this._extruded
          ? "mapboxgl-ctrl-icon mapboxgl-ctrl-2d"
          : "mapboxgl-ctrl-icon mapboxgl-ctrl-3d";
        $("#3d-button").prop("class", className);

        _this.redraw();
        _this.deckgl.setProps({
          controller: { dragRotate: this._extruded },
          viewState: {
            ..._this.currentViewState,
            pitch: pitch,
            bearing: bearing,
            transitionDuration: 300
          }
        });
      };

      this._container = document.createElement("div");
      this._container.className = "mapboxgl-ctrl-group mapboxgl-ctrl";
      this._container.appendChild(this._btn);

      return this._container;
    }

    onRemove() {
      this._container.parentNode.removeChild(this._container);
      this._map = undefined;
    }
  }

  class darkToggle {
    constructor() {
      this._dark = false;
    }
    onAdd(map) {
      this._map = map;

      this._btn = document.createElement("button");
      this._btn.id = "dark-button";
      this._btn.className = "mapboxgl-ctrl-icon mapboxgl-ctrl-map-style";
      this._btn.type = "button";
      this._btn.setAttribute("data-toggle", "tooltip");
      this._btn.setAttribute("data-placement", "left");
      this._btn.setAttribute("data-container", "body");
      this._btn.setAttribute("data-trigger", "hover");
      this._btn.setAttribute("title", "Toggle Dark map");
      this._btn.onclick = function() {
        this._dark = !this._dark;
        if (this._dark) {
          _this.deckgl.getMapboxMap().setStyle(_this.mapStyles.dark);
        } else {
          _this.deckgl.getMapboxMap().setStyle(_this.mapStyles.light);
        }
      };

      this._container = document.createElement("div");
      this._container.className = "mapboxgl-ctrl-group mapboxgl-ctrl";
      this._container.appendChild(this._btn);

      return this._container;
    }

    onRemove() {
      this._container.parentNode.removeChild(this._container);
      this._map = undefined;
    }
  }

  class recenterMap {
    onAdd(map) {
      this._map = map;

      this._btn = document.createElement("button");
      this._btn.id = "recenter-button";
      this._btn.className = "mapboxgl-ctrl-icon mapboxgl-ctrl-recenter";
      this._btn.type = "button";
      this._btn.setAttribute("data-toggle", "tooltip");
      this._btn.setAttribute("data-placement", "left");
      this._btn.setAttribute("data-container", "body");
      this._btn.setAttribute("data-trigger", "hover");
      this._btn.setAttribute("title", "Center to location");
      this._btn.onclick = function() {
        _this.deckgl.setProps({
          viewState: {
            ..._this.currentViewState,
            zoom: _this.cameraOptions.zoom,
            latitude: _this.cameraOptions.center.lat,
            longitude: _this.cameraOptions.center.lng,
            transitionDuration: 300
          }
        });
      };

      this._container = document.createElement("div");
      this._container.className = "mapboxgl-ctrl-group mapboxgl-ctrl";
      this._container.appendChild(this._btn);

      return this._container;
    }

    onRemove() {
      this._container.parentNode.removeChild(this._container);
      this._map = undefined;
    }
  }

  class showLayerToggle {
    constructor() {
      this._show = false;
    }
    onAdd(map) {
      this._map = map;

      this._btn = document.createElement("button");
      this._btn.id = "layer-toggle-button";
      this._btn.className = "mapboxgl-ctrl-icon mapboxgl-ctrl-layer-toggle";
      this._btn.type = "button";
      this._btn.setAttribute("data-toggle", "tooltip");
      this._btn.setAttribute("data-placement", "left");
      this._btn.setAttribute("data-container", "body");
      this._btn.setAttribute("data-trigger", "hover");
      this._btn.setAttribute("title", "Show layer toggle");
      this._btn.onclick = function() {
        this._show = !this._show;
        if (this._show) {
          document.getElementById("layers-group").style.visibility = "visible";
        } else {
          document.getElementById("layers-group").style.visibility = "hidden";
        }
      };

      this._container = document.createElement("div");
      this._container.className = "mapboxgl-ctrl-group mapboxgl-ctrl";
      this._container.appendChild(this._btn);

      return this._container;
    }

    onRemove() {
      this._container.parentNode.removeChild(this._container);
      this._map = undefined;
    }
  }

  _this.deckgl.getMapboxMap().addControl(new dToggle(), "top-right");
  _this.deckgl.getMapboxMap().addControl(new darkToggle(), "top-right");
  _this.deckgl.getMapboxMap().addControl(new recenterMap(), "top-right");
  _this.deckgl.getMapboxMap().addControl(new showLayerToggle(), "top-right");
  _this.deckgl.setProps({
    onDragStart: (info, event) => {
      let dToggleButton = $("#3d-button");
      if (
        event.rightButton &&
        dToggleButton.attr("data-extruded") === "false"
      ) {
        dToggleButton.trigger("click");
      }
    }
  });
}

function updateTooltip({ x, y, object, layer }) {
  const tooltip = document.getElementById(`map-tooltip`);
  if (object) {
    tooltip.style.top = `${y}px`;
    tooltip.style.left = `${x}px`;
    let innerHTML = "";

    if (layer.id === "zone" || layer.id === "surroundings") {
      $.each(object.properties, function(key, value) {
        innerHTML += `<div><b>${key}</b>: ${value}</div>`;
      });
      let area = turf.area(object);
      innerHTML +=
        `<br><div><b>area</b>: ${Math.round(area * 1000) /
          1000}m<sup>2</sup></div>` +
        `<div><b>volume</b>: ${Math.round(
          area * object.properties["height_ag"] * 1000
        ) / 1000}m<sup>3</sup></div>`;
    } else if (layer.id === "dc" || layer.id === "dh") {
      $.each(object.properties, function(key, value) {
        if (key !== "Building" && value === "NONE") return null;
        innerHTML += `<div><b>${key}</b>: ${value}</div>`;
      });
      if (!object.properties.hasOwnProperty("Building")) {
        let length = turf.length(object) * 1000;
        innerHTML += `<br><div><b>length</b>: ${Math.round(length * 1000) /
          1000}m</div>`;
      }
    } else {
      $.each(object.properties, function(key, value) {
        innerHTML += `<div><b>${key}</b>: ${value}</div>`;
      });
    }

    tooltip.innerHTML = innerHTML;
  } else {
    tooltip.innerHTML = "";
  }
}

function nodeFillColor(type, network) {
  if (type === "NONE") {
    return network === "dc" ? defaultColors.dc : defaultColors.dh;
  } else if (type === "CONSUMER") {
    return [255, 255, 255];
  } else if (type === "PLANT") {
    return [0, 0, 0];
  }
}

var MapWidget = (function (options) {

    /**
     * 
     * @param {any} plHash
     */
    // see https://github.com/geoext/geoext/blob/f4c4b252d13e6737f4c4da9437eee09067132327/classic/state/PermalinkProvider.js
    function readPermalinkHash(plHash) {
        var mapState;
        // try to restore center, zoom-level and rotation from the URL
        var hash = plHash.replace('#map=', '');
        var parts = hash.split('/');

        if (parts.length === 4) {
            mapState = {
                zoom: parseInt(parts[0], 10),
                center: [
                    parseFloat(parts[1]),
                    parseFloat(parts[2])
                ],
                rotation: parseFloat(parts[3])
            };
        }

        return mapState;
    }

    proj4.defs('EPSG:2157', '+proj=tmerc +lat_0=53.5 +lon_0=-8 +k=0.99982 +x_0=600000 +y_0=750000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs');
    ol.proj.proj4.register(proj4);

    var me = {};

    // Allow these properties to be set when creating the widget

    options = options ? options : {};

    var msURL = options.msURL ? options.msURL : 'https://mapserver.compass.ie/mapserver/?map=H:/MapServer/apps/hydro/hydro.map&';
    var permalink = options.permalink ? options.permalink : '#map=16.18731868456231/-879496.96/6883726.35/0';
    var mapState = readPermalinkHash(permalink);

    var center = mapState.center;
    var zoom = mapState.zoom;

    var divName = options.divName ? options.divName : 'map';
    var layerVisibilities = options.layerVisibilities ? options.layerVisibilities : {};

    var attributions = [];

    var basemaps = new ol.layer.Group({
        title: 'Base maps',
        layers: [new ol.layer.Tile({
            title: 'OSM',
            source: new ol.source.OSM(),
            projection: "EPSG:3857",
            className: 'bw',
        })
        ]
    });

    var layersList = [

        { key: 'Strahler', title: 'Strahler', opacity: 0.9, style: '' },
        { key: 'StrahlerLabels', title: 'Strahler Orders', style: '' },
        { key: 'Shreve', title: 'Shreve', opacity: 0.9, style: '' },
        { key: 'ShreveLabels', title: 'Shreve Orders', opacity: 0.9, style: '' },
        { key: 'Flow', title: 'Flow Direction', opacity: 0.9, style: '' },
        { key: 'Sinks', title: 'Sinks', opacity: 0.9, style: '' },
        { key: 'SinkCodes', title: 'Sink Codes', opacity: 0.9, style: '' },
        { key: 'SourceCodes', title: 'SourceCodes', opacity: 0.9, style: '' },
    ]

    var layers = [];

    var lyr, src, style;
    layersList.forEach(function (l) {

        // if not one of the listed layers then it should not be added to the widget

        var foundLayer = layerVisibilities[l.key];

        if (!foundLayer) {
            return;
        }

        src = l.src ? l.src : l.key;
        style = l.style ? l.style : '';

        lyr = new ol.layer.Image({
            opacity: l.opacity ? l.opacity : 0.6,
            title: l.title,
            visible: false,
            source: new ol.source.ImageWMS({
                url: msURL,
                params: {
                    'LAYERS': [src],
                    'STYLES': [style]
                }
            })
        });
        layers.push(lyr);
    });

    var overlaysGroup = new ol.layer.Group({
        title: 'Overlays',
        layers: layers
    });

    var map = new ol.Map({
        controls: ol.control.defaults.defaults({ attribution: false }).extend([
            new ol.control.FullScreen(),
            new ol.control.Attribution({
                collapsible: false
            })
        ]),
        layers: [basemaps, overlaysGroup],
        target: divName,
        view: new ol.View({
            projection: 'EPSG:2157',
            center: center,
            zoom: zoom
        })
    });

    // http://www.acuriousanimal.com/thebookofopenlayers3/chapter02_03_layer_groups.html
    function findBy(layer, key) {

        var layerCfg = layersList.find(function (obj) {
            return obj.key === key;
        });

        if (!layerCfg) {
            console.error('Layer with key ' + key + ' not found');
        }

        var src = layerCfg.src ? layerCfg.src : layerCfg.key;
        var style = layerCfg.style ? layerCfg.style : '';

        if (layer.getSource && layer.getSource().getParams) {
            var params = layer.getSource().getParams();
            if ((params.LAYERS[0] === src) && (params.STYLES[0] === style)) {
                return layer;
            }
        }

        // Find recursively if it is a group
        if (layer.getLayers) {
            var layers = layer.getLayers().getArray(),
                len = layers.length, result;
            for (var i = 0; i < len; i++) {
                result = findBy(layers[i], key);
                if (result) {
                    return result;
                }
            }
        }
        return null;
    }

    var layerGroup = map.getLayerGroup();
    var l;

    $.each(layerVisibilities, function (key, value) {
        l = findBy(layerGroup, key);
        if (l !== null) {
            l.setVisible(value);
        }
    });

    var layerSwitcher = new ol.control.LayerSwitcher();
    map.addControl(layerSwitcher);

    return me;
});

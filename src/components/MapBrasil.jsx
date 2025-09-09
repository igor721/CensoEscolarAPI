import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";

const geojsonURL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

function MapBrasil({ ano, onEstadoClick }) {
  const [geoData, setGeoData] = useState(null);

  useEffect(() => {
    axios.get(geojsonURL)
      .then(response => setGeoData(response.data))
      .catch(err => console.error("Erro ao carregar GeoJSON", err));
  }, []);

  function estiloFeature(feature) {
    return {
      fillColor: "#FD8D3C",
      weight: 2,
      opacity: 1,
      color: "white",
      dashArray: "3",
      fillOpacity: 0.7
    };
  }

  function onEachFeature(feature, layer) {
    layer.on({
      click: () => {
        onEstadoClick(feature.properties.name);
      }
    });
    layer.bindTooltip(feature.properties.name, { sticky: true });
  }

  return (
    <div style={{ width: "50vw", height: "600px" }}>
      {geoData && (
        <MapContainer center={[-15.78, -47.93]} zoom={4} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <GeoJSON data={geoData} style={estiloFeature} onEachFeature={onEachFeature} />
        </MapContainer>
      )}
    </div>
  );
}

export default MapBrasil;
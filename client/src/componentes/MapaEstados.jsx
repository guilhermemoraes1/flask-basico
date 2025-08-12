import React, { useEffect, useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
} from "react-simple-maps";

const stateViewConfig = {
  AC: { center: [-70.5, -9.0], scale: 5000 },
  AL: { center: [-36.5, -9.5], scale: 11000 },
  AM: { center: [-64.5, -4.0], scale: 2500 },
  AP: { center: [-51.5, 1.0], scale: 5000 },
  BA: { center: [-40.5, -13.5], scale: 3000 },
  CE: { center: [-39.5, -5.5], scale: 6800 },
  DF: { center: [-47.7, -15.8], scale: 25000 },
  ES: { center: [-40.5, -19.5], scale: 10000 },
  GO: { center: [-49.5, -16.0], scale: 5000 },
  MA: { center: [-45.0, -6.5], scale: 4000 },
  MG: { center: [-45.5, -19.0], scale: 3000 },
  MS: { center: [-54.5, -21.0], scale: 5000 },
  MT: { center: [-56.0, -14.0], scale: 3000 },
  PA: { center: [-52.0, -5.0], scale: 2500 },
  PB: { center: [-36.5, -7.8], scale: 9500 },
  PR: { center: [-51.0, -25.5], scale: 6000 },
  PE: { center: [-37.8, -9.0], scale: 6000 },
  PI: { center: [-43.0, -7.0], scale: 4500 },
  RJ: { center: [-42.6, -22.6], scale: 10000 },
  RN: { center: [-36.7, -6.5], scale: 10000 },
  RO: { center: [-63.0, -11.5], scale: 5600 },
  RR: { center: [-61.0, 2.0], scale: 5000 },
  RS: { center: [-53.0, -30.4], scale: 4500 },
  SC: { center: [-50.4, -28.5], scale: 6000 },
  SE: { center: [-37.5, -10.5], scale: 17000 },
  SP: { center: [-48.0, -23.5], scale: 4000 },
  TO: { center: [-48.5, -9.0], scale: 5000 },
};

const MapaEstados = ({ sigla, ano }) => {
  const [geoData, setGeoData] = useState(null);
  const [dadosMunicipios, setDadosMunicipios] = useState({});
  const [tooltip, setTooltip] = useState("");

  const getColor = (valor) => {
    if (!valor) return "#e0e0e0";
    if (valor > 90000) return "#0d47a1";
    if (valor > 60000) return "#1565c0";
    if (valor > 40000) return "#1976d2";
    if (valor > 25000) return "#1e88e5";
    if (valor > 18000) return "#42a5f5";
    if (valor > 12000) return "#64b5f6";
    if (valor > 8000) return "#81d4fa";
    if (valor > 5000) return "#90caf9";
    if (valor > 3000) return "#bbdefb";
    return "#e3f2fd";
  };

  const geoJsonUrls = (sigla) =>
    `https://raw.githubusercontent.com/luizpedone/municipal-brazilian-geodata/refs/heads/master/minified/${sigla}.min.json`;

  useEffect(() => {
    const url = geoJsonUrls(sigla);

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`Erro ao carregar GeoJSON para ${sigla}`);
        return res.json();
      })
      .then(setGeoData)
      .catch((err) => {
        console.error("Erro ao carregar GeoJSON:", err);
        setGeoData(null);
      });
  }, [sigla]);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/dados/municipios${ano}?uf=${sigla}`)
      .then((res) => res.json())
      .then((data) => {
        const filtrado = data.filter((item) => item.sg_uf === sigla);
        const formatado = {};
        filtrado.forEach((item) => {
          formatado[item.co_municipio] = item.mat_bas;
        });
        setDadosMunicipios(formatado);
      })
      .catch((err) => {
        console.error("Erro ao carregar dados dos municípios:", err);
        setDadosMunicipios({});
      });
  }, [sigla, ano]);

  if (!geoData) return <div>Carregando mapa de {sigla}...</div>;

  const config = stateViewConfig[sigla] || { center: [-55, -15], scale: 2000 };

  return (
    <>
    <ComposableMap
      projection="geoMercator"
      projectionConfig={{
        scale: config.scale,
        center: config.center,
      }}
      width={800}
      height={800}
    >
      <ZoomableGroup>
        <Geographies geography={geoData}>
          {({ geographies }) =>
            geographies.map((geo) => {
              const codigoMun = parseInt(geo.properties.GEOCODIGO, 10);
              const valor = dadosMunicipios[codigoMun];

              return (
                <Geography
                  key={geo.rsmKey || codigoMun}
                  geography={geo}
                  onMouseEnter={() => {
                  setTooltip(
                      valor
                      ? `${geo.properties.NOME}: ${valor.toLocaleString()} matrículas`
                      : `${geo.properties.NOME}: sem dados`
                  );
                  }}
                  onMouseLeave={() => {
                  setTooltip("");
                  }}
                  style={{
                    default: {
                      fill: getColor(valor),
                      outline: "none",
                    },
                    hover: {
                      fill: getColor(valor),
                      outline: "none",
                      stroke: "#fff",
                      strokeWidth: 1.5,
                      cursor: "pointer",
                    },
                    pressed: {
                      fill: getColor(valor),
                      outline: "none",
                      stroke: "#333",
                      strokeWidth: 2,
                    },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ZoomableGroup>
    </ComposableMap>
    <div style={{ marginTop: 20, fontSize: "1.2rem", fontWeight: "bold" }}>
      {tooltip}
    </div>
    </>
  );
};

export default MapaEstados;
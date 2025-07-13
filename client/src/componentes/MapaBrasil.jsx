import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
} from "react-simple-maps";
import MapaEstados from "./MapaEstados"; // ou o caminho correto

// URL do GeoJSON do mapa do Brasil
const geoUrl =
  "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const MapaBrasil = () => {
  const getColor = (valor) => {
    if (!valor) return "#e0e0e0"; // sem dados
    if (valor > 10_000_000) return "#0d47a1";      // SP
    if (valor > 5_500_000)  return "#1565c0";      // RJ e MG
    if (valor > 3_000_000)  return "#1976d2";      // BA, PR
    if (valor > 2_000_000)  return "#1e88e5";      // RS, PA, CE, PE
    if (valor > 1_500_000)  return "#42a5f5";      // GO, AM
    if (valor > 1_000_000)  return "#64b5f6";      // MA, SC
    if (valor > 850_000)    return "#81d4fa";      // ES, AL, MT
    if (valor > 700_000)    return "#90caf9";      // PB, DF
    if (valor > 500_000)    return "#bbdefb";      // PI, MS, RN, SE
    if (valor > 250_000)    return "#d0eaff";      // AC, RO
    return "#e3f2fd";                              // TO, AP, RR
  };


  const [dados, setDados] = useState({});
  const [tooltip, setTooltip] = useState("");
  const [ano, setAno] = useState("2023"); // estado para controlar o ano selecionado
  const [estadoSelecionado, setEstadoSelecionado] = useState("");

  useEffect(() => {
    // Atualiza a API conforme o ano selecionado
    axios
      .get(`http://127.0.0.1:5000/dados/estados${ano}`)
      .then((response) => {
        const dadosFormatados = {};
        response.data.forEach((item) => {
          dadosFormatados[item.sg_uf] = item.mat_bas;
        });
        setDados(dadosFormatados);
      })
      .catch((error) => {
        console.error("Erro ao buscar dados dos estados:", error);
        setDados({});
      });
  }, [ano]); // reexecuta quando o ano mudar

  return (
    <div>
        <div style={{ marginBottom: 20 }}>
            <label htmlFor="selectAno">Escolha o ano: </label>
            <select
                id="selectAno"
                value={ano}
                onChange={(e) => setAno(e.target.value)}
            >
                <option value="2023">2023</option>
                <option value="2024">2024</option>
            </select>
        </div>

        <div style={{ marginBottom: 20 }}>
            <label htmlFor="selectEstado">Escolha o estado: </label>
            <select
                id="selectEstado"
                value={estadoSelecionado}
                onChange={(e) => setEstadoSelecionado(e.target.value)}
            >
                <option value="">Todos os estados</option>
                <option value="AC">Acre</option>
                <option value="AL">Alagoas</option>
                <option value="AP">Amapá</option>
                <option value="AM">Amazonas</option>
                <option value="BA">Bahia</option>
                <option value="CE">Ceará</option>
                <option value="DF">Distrito Federal</option>
                <option value="ES">Espírito Santo</option>
                <option value="GO">Goiás</option>
                <option value="MA">Maranhão</option>
                <option value="MT">Mato Grosso</option>
                <option value="MS">Mato Grosso do Sul</option>
                <option value="MG">Minas Gerais</option>
                <option value="PA">Pará</option>
                <option value="PB">Paraíba</option>
                <option value="PR">Paraná</option>
                <option value="PE">Pernambuco</option>
                <option value="PI">Piauí</option>
                <option value="RJ">Rio de Janeiro</option>
                <option value="RN">Rio Grande do Norte</option>
                <option value="RS">Rio Grande do Sul</option>
                <option value="RO">Rondônia</option>
                <option value="RR">Roraima</option>
                <option value="SC">Santa Catarina</option>
                <option value="SP">São Paulo</option>
                <option value="SE">Sergipe</option>
                <option value="TO">Tocantins</option>

            </select>
        </div>

        {estadoSelecionado === "" ? (
        <>
            <ComposableMap
                projection="geoMercator"
                projectionConfig={{
                scale: 2450,
                center: [-55, -15],
                }}
                width={2000}
                height={2000}
            >
                <ZoomableGroup
                translateExtent={[
                    [-20, -20],
                    [1900, 1900],
                ]}
                >
                <Geographies geography={geoUrl}>
                    {({ geographies }) =>
                    geographies.map((geo) => {
                        const siglaUF = geo.properties.sigla;
                        const valorMatricula = dados[siglaUF];

                        return (
                        <Geography
                            key={geo.rsmKey}
                            geography={geo}
                            onMouseEnter={() => {
                            setTooltip(
                                valorMatricula
                                ? `${siglaUF}: ${valorMatricula.toLocaleString()} matrículas`
                                : `${siglaUF}: sem dados`
                            );
                            }}
                            onMouseLeave={() => {
                            setTooltip("");
                            }}
                            style={{
                            default: {
                                fill: getColor(valorMatricula),
                                outline: "none",
                            },
                            hover: {
                                fill: getColor(valorMatricula),
                                outline: "none",
                                stroke: "#fff",
                                strokeWidth: 1.5,
                                cursor: "pointer",
                            },
                            pressed: {
                                fill: getColor(valorMatricula),
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
        ) : (
        <MapaEstados sigla={estadoSelecionado} ano={ano} />
        )}



      
      <div
        style={{ marginTop: 20, fontSize: "1.2rem", fontWeight: "bold" }}
      >
        {tooltip}
      </div>
    </div>
  );
};

export default MapaBrasil;

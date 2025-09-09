import React, { useState, useEffect } from "react";
import axios from "axios";
import MapBrasil from "./components/MapBrasil";

const API_BASE_URL = "http://127.0.0.1:5000"; 

const anosDisponiveis = [2024, 2023]; 

function App() {
  const [ano, setAno] = useState(2023);
  const [estadoSelecionado, setEstadoSelecionado] = useState("Rio de Janeiro");
  const [censoInfo, setCensoInfo] = useState(null);

  useEffect(() => {
    if (estadoSelecionado) {
      axios.get(`${API_BASE_URL}/censoescolar`, {
        params: {
          estado: estadoSelecionado,
          ano,
        }
      })
      .then(response => setCensoInfo(response.data))
      .catch(err => console.error("Erro ao buscar dados do censo", err));
    }
  }, [estadoSelecionado, ano]);

  return (
    <div style={{ padding: "20px" }}>
      <div style={{ marginBottom: "16px" }}>
        <label>Ano: </label>
        <select value={ano} onChange={e => setAno(Number(e.target.value))}>
          {anosDisponiveis.map(a => (
            <option key={a} value={a}>{a}</option>
          ))}
        </select>

        <label style={{ marginLeft: "16px" }}>Estado: </label>
        <select value={estadoSelecionado} onChange={e => setEstadoSelecionado(e.target.value)}>
          {[
            "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia",
            "Ceará", "Distrito Federal", "Espírito Santo", "Goiás",
            "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais",
            "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
            "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul",
            "Rondônia", "Roraima", "Santa Catarina", "São Paulo",
            "Sergipe", "Tocantins"
          ].map(estado => (
            <option key={estado} value={estado}>{estado}</option>
          ))}
        </select>
      </div>

      <div style={{ display: "flex", alignItems: "flex-start", gap: "40px" }}>
        <div style={{ flex: "1 1 60%" }}>
          <MapBrasil ano={ano} onEstadoClick={setEstadoSelecionado} />
        </div>

        <div style={{ flex: "1 1 40%", maxWidth: "400px" }}>
          <h2>Informações do Censo Escolar - {estadoSelecionado} ({ano})</h2>
          {censoInfo ? (
            <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
              {JSON.stringify(censoInfo, null, 2)}
            </pre>
          ) : (
            <p>Selecione um estado para ver as informações.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login/Login';
import Cadastro from './pages/Cadastro/Cadastro';

function App() {
  return (
    <Router>
      <Routes>
        {/* Se o usuário acessar a raiz "/", ele é mandado para o Login */}
        <Route path="/" element={<Navigate to="/login" />} />
        
        {/* Rotas declaradas */}
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        
        {/* Rota de segurança para qualquer link errado (opcional) */}
        <Route path="*" element={<h2>Página não encontrada (404)</h2>} />
      </Routes>
    </Router>
  );
}

export default App;
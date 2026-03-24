import React, { useState } from 'react';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';
import '../../index.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mensagem, setMensagem] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await api.post('/login', formData);
      
        localStorage.setItem('user', response.data.user);
        setMensagem("Acesso concedido!");
        setTimeout(() => {
            navigate('/dashboard');
        }, 1000);
    } catch (error) {
        if (error.response && error.response.status === 403) {
            setMensagem("Sua conta ainda não foi ativada. Verifique seu e-mail.");
        } else {
            setMensagem("Usuário ou senha incorretos.");
        }
    }
  };

  return (
    <div className="orca-card">
      <h2 style={{ textAlign: 'center', marginBottom: '24px' }}>Entrar no ORCA</h2>
      <form onSubmit={handleLogin}>
        <input 
          className="orca-input"
          type="text" placeholder="Usuário" 
          onChange={(e) => setUsername(e.target.value)} 
          required
        />
        <input 
          className="orca-input"
          type="password" placeholder="Senha" 
          onChange={(e) => setPassword(e.target.value)} 
          required
        />
        <button className="orca-button" type="submit">Acessar Sistema</button>
      </form>
      
      {mensagem && <p style={{ textAlign: 'center', color: '#f6465d' }}>{mensagem}</p>}
      
      <span className="orca-link" onClick={() => navigate('/cadastro')}>
        Não tem uma conta? Cadastre-se agora
      </span>
    </div>
  );
}

export default Login;
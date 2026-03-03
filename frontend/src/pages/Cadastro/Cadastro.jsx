import React, { useState } from 'react';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';
import '../../index.css';

function Cadastro() {
    const [formData, setFormData] = useState({
        nome: '',
        sobrenome: '',
        email: '',
        username: '',
        password: '',
        password_confirm: ''
    });
    const [etapa, setEtapa] = useState(1);
    const [codigoVerificacao, setCodigoVerificacao] = useState('');
    const [mensagem, setMensagem] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleCadastro = async (e) => {
        e.preventDefault();
        const data = new FormData();
        Object.keys(formData).forEach(key => data.append(key, formData[key]));

        try {
            await api.post('/cadastro', data);
            setMensagem("Conta pré-cadastrada! Verifique o terminal do backend.");
            setEtapa(2); 
        } catch (error) {
            setMensagem(error.response?.data?.detail || "Erro ao cadastrar");
        }
    };

    const handleVerificar = async (e) => {
        e.preventDefault();
        const data = new FormData();
        data.append('email', formData.email);
        data.append('codigo', codigoVerificacao);

        try {
            const res = await api.post('/verificar-codigo', data);
            setMensagem("Sucesso! Ativando conta...");
            setTimeout(() => navigate('/login'), 2000);
        } catch (error) {
            setMensagem("Código inválido ou incorreto.");
        }
    };

    return (
        <div className="orca-card">
            <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>
                {etapa === 1 ? "Criar Conta ORCA" : "Verificar E-mail"}
            </h2>

            {etapa === 1 ? (
                <form onSubmit={handleCadastro}>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input className="orca-input" name="nome" placeholder="Nome" onChange={handleChange} required />
                        <input className="orca-input" name="sobrenome" placeholder="Sobrenome" onChange={handleChange} required />
                    </div>
                    <input className="orca-input" name="email" type="email" placeholder="E-mail" onChange={handleChange} required />
                    <input className="orca-input" name="username" placeholder="Usuário" onChange={handleChange} required />
                    <input className="orca-input" name="password" type="password" placeholder="Senha" onChange={handleChange} required />
                    <input className="orca-input" name="password_confirm" type="password" placeholder="Repita a Senha" onChange={handleChange} required />
                    
                    <button className="orca-button" type="submit">Finalizar Cadastro</button>
                </form>
            ) : (
                <form onSubmit={handleVerificar}>
                    <p style={{ textAlign: 'center', color: '#b7bdc6' }}>Digite o código enviado para {formData.email}</p>
                    <input 
                        className="orca-input"
                        type="text" 
                        placeholder="000000" 
                        maxLength="6"
                        onChange={(e) => setCodigoVerificacao(e.target.value)} 
                        style={{ fontSize: '24px', textAlign: 'center', letterSpacing: '8px' }}
                        required 
                    />
                    <button className="orca-button" type="submit">Ativar Conta</button>
                </form>
            )}

            {mensagem && (
                <p style={{ 
                    marginTop: '15px', 
                    textAlign: 'center', 
                    color: mensagem.includes('Erro') || mensagem.includes('inválido') ? '#f6465d' : '#2ebd85' 
                }}>
                    {mensagem}
                </p>
            )}

            <span className="orca-link" onClick={() => navigate('/login')}>
                Já tem uma conta? Entrar
            </span>
        </div>
    );
}

export default Cadastro;
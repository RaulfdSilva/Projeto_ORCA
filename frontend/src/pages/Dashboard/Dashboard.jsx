import React, { useEffect, useState, useRef } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { createChart } from 'lightweight-charts';
import api from '../../services/api';
import './Dashboard.css';

const dadosAlocacao = [
    { name: 'BTC', value: 45, color: '#f0b90b' },
    { name: 'ETH', value: 30, color: '#627eea' },
    { name: 'SOL', value: 15, color: '#dc1fff' },
    { name: 'USDT', value: 10, color: '#2ebd85' },
];

const mockNews = [
    { id: 1, text: "Binance anuncia nova parceria institucional para custódia.", sentiment: "bullish", source: "Reuters" },
    { id: 2, text: "FED sinaliza manutenção das taxas de juros para o próximo mês.", sentiment: "neutral", source: "Bloomberg" },
    { id: 3, text: "Baleias movimentam 50k BTC para exchanges de forma súbita.", sentiment: "bearish", source: "WhaleAlert" },
];

function Dashboard() {
    const chartContainerRef = useRef();
    const [moeda, setMoeda] = useState('BTC');
    const [userName, setUserName] = useState('RaulFDSilva');
    const [logs, setLogs] = useState([]);
    const [news, setNews] = useState(mockNews);

    useEffect(() => {
        const interval = setInterval(() => {
            const time = new Date().toLocaleTimeString();
            setLogs(prev => [`[${time}] NLP Module: Analyzing news sentiment...`, ...prev].slice(0, 3));
        }, 7000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (!chartContainerRef.current) return;
        chartContainerRef.current.innerHTML = '';
        const chart = createChart(chartContainerRef.current, {
            layout: { background: { color: 'transparent' }, textColor: '#848e9c' },
            grid: { vertLines: { color: 'rgba(255,255,255,0.03)' }, horzLines: { color: 'rgba(255,255,255,0.03)' } },
            width: chartContainerRef.current.clientWidth,
            height: 340,
        });
        const candleSeries = chart.addCandlestickSeries({
            upColor: '#00f2ff', downColor: '#bc00ff', borderVisible: false,
            wickUpColor: '#00f2ff', wickDownColor: '#bc00ff',
        });

        const fetchCandles = async () => {
            try {
                const res = await api.get(`/api/historico/${moeda}`);
                candleSeries.setData(res.data.map(d => ({
                    time: Math.floor(d.time / 1000),
                    open: d.open, high: d.high, low: d.low, close: d.close
                })).sort((a, b) => a.time - b.time));
            } catch (e) { console.error(e); }
        };

        fetchCandles();
        return () => chart.remove();
    }, [moeda]);

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div>
                    <h2 style={{ margin: 0, fontSize: '18px' }}>Olá, <span className="user-name">{userName}</span>!</h2>
                    <span style={{ color: '#848e9c', fontSize: '11px' }}>
                        <div className="status-indicator"></div> Sistema ORCA Online - Inteligência Preditiva & NLP
                    </span>
                </div>
                <button className="logout-button" onClick={() => window.location.href = '/login'}>Sair</button>
            </header>

            <main className="allocation-section">
                {/* COLUNA 1: ALOCAÇÃO */}
                <div className="card-base side-card">
                    <h4 style={{ color: '#848e9c', margin: '0 0 10px 0', fontSize: '13px' }}>Distribuição</h4>
                    <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                            <Pie data={dadosAlocacao} cx="50%" cy="50%" innerRadius="60%" outerRadius="85%" dataKey="value">
                                {dadosAlocacao.map((entry, index) => <Cell key={index} fill={entry.color} stroke="none" />)}
                            </Pie>
                        </PieChart>
                    </ResponsiveContainer>
                    <div style={{ marginTop: '10px', fontSize: '11px' }}>
                        {dadosAlocacao.map((d, i) => (
                            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                                <span style={{ color: '#848e9c' }}>{d.name}</span><strong>{d.value}%</strong>
                            </div>
                        ))}
                    </div>
                </div>

                {/* COLUNA 2: ANÁLISE TÉCNICA (MAIN) */}
                <div className="card-base main-card">
                    <div className="trading-card-header">
                        <h4 style={{ margin: 0, fontSize: '14px' }}>Mercado {moeda}/USDT</h4>
                        <div className="orca-select-container">
                            <select className="orca-input-select" value={moeda} onChange={(e) => setMoeda(e.target.value)}>
                                <option value="BTC">BTC</option><option value="ETH">ETH</option><option value="SOL">SOL</option>
                            </select>
                        </div>
                    </div>
                    <div ref={chartContainerRef} style={{ width: '100%', height: '340px' }} />
                </div>

                {/* COLUNA 3: NLP SENTIMENT (NOVO) */}
                <div className="card-base side-card">
                    <h4 style={{ color: '#848e9c', margin: '0 0 5px 0', fontSize: '13px' }}>Análise de Notícias</h4>
                    <div className="news-feed">
                        {news.map(item => (
                            <div key={item.id} className={`news-item sent-${item.sentiment}`}>
                                <strong>{item.source}</strong>: {item.text}
                                <br />
                                <span className="sentiment-tag" style={{ 
                                    color: item.sentiment === 'bullish' ? '#2ebd85' : item.sentiment === 'bearish' ? '#f6465d' : '#f0b90b' 
                                }}>
                                    {item.sentiment}
                                </span>
                            </div>
                        ))}
                    </div>
                    <div style={{ marginTop: 'auto', fontSize: '10px', textAlign: 'center', color: '#848e9c' }}>
                        IA processando sentimento via Python...
                    </div>
                </div>
            </main>

            {/* RODAPÉ: MONITORAMENTO E LOGS */}
            <section className="card-base ai-monitor-card">
                <div style={{ display: 'flex', gap: '30px', alignItems: 'center', height: '100%' }}>
                    <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                            <span style={{ color: '#00f2ff', fontWeight: 'bold' }}>ORCA CORE: DATA MINING</span>
                            <span style={{ color: '#848e9c' }}>ESTADO: PROCESSANDO</span>
                        </div>
                        <div className="progress-bar-bg"><div className="progress-bar-fill" style={{ width: '62%' }}></div></div>
                    </div>
                    <div style={{ flex: 1 }}>
                        <div className="system-logs">
                            {logs.map((log, i) => <div key={i}>{log}</div>)}
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Dashboard;
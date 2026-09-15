"use client";

import { useMemo, useState } from "react";

type Resultado = {
  geracoes: number; melhor_individuo: string; x: number; aptidao: number;
  cromossomo_binario: string; populacao_inicial: string[];
  populacao_final: string[]; convergiu: boolean;
};

const API_URL = "http://localhost:8000";

function Individuo({ cromossomo, destaque = false }: { cromossomo: string; destaque?: boolean }) {
  return <div className={destaque ? "individuo destaque" : "individuo"}>
    <span className="bits">{cromossomo}</span><span className="decimal">x = {parseInt(cromossomo, 2)}</span>
  </div>;
}

export default function Home() {
  const [resultado, setResultado] = useState<Resultado | null>(null);
  const [executando, setExecutando] = useState(false);
  const [erro, setErro] = useState("");

  const melhorInicial = useMemo(() => {
    if (!resultado) return null;
    let melhor = resultado.populacao_inicial[0];
    let melhorValor = -Infinity;
    for (const cromossomo of resultado.populacao_inicial) {
      const x = parseInt(cromossomo, 2);
      const aptidao = x * Math.sin(x / 20) + 100;
      if (aptidao > melhorValor) { melhorValor = aptidao; melhor = cromossomo; }
    }
    return melhor;
  }, [resultado]);

  async function executar() {
    setExecutando(true); setErro("");
    try {
      const resposta = await fetch(`${API_URL}/executar`, { method: "POST" });
      if (!resposta.ok) throw new Error();
      setResultado(await resposta.json());
    } catch {
      setErro("Não foi possível acessar o Python. Inicie o servidor do backend e tente novamente.");
    } finally { setExecutando(false); }
  }

  return <main>
    <section className="hero">
      <nav><div className="marca"><span>AG</span> Laboratório Evolutivo</div><div className="status"><i /> Algoritmo configurado</div></nav>
      <div className="hero-grid">
        <div>
          <p className="sobretitulo">INTELIGÊNCIA ARTIFICIAL · TRABALHO 01</p>
          <h1>Encontrando o máximo por <em>evolução.</em></h1>
          <p className="introducao">Observe uma população de soluções competir, cruzar seus cromossomos e evoluir até encontrar o máximo global da função.</p>
          <button onClick={executar} disabled={executando}>{executando ? "Evoluindo população..." : "Executar algoritmo"}<span>→</span></button>
          {erro && <p className="erro">{erro}</p>}
        </div>
        <div className="formula-card">
          <span className="card-label">FUNÇÃO DE APTIDÃO</span><div className="formula">f(x) = x · sen(x/20) + 100</div><div className="dominio">0 ≤ x ≤ 511</div>
          <div className="onda" aria-hidden="true"><span /><span /><span /><span /><span /></div>
        </div>
      </div>
    </section>

    <section className="configuracoes">
      <div><strong>40</strong><span>indivíduos</span></div><div><strong>9</strong><span>bits</span></div><div><strong>20</strong><span>filhos / geração</span></div><div><strong>3%</strong><span>mutação</span></div><div><strong>10.000</strong><span>gerações máximas</span></div>
    </section>

    {resultado ? <section className="resultados">
      <div className="section-heading"><div><p className="sobretitulo">RESULTADO DA EXECUÇÃO</p><h2>A seleção natural em números</h2></div><span className={resultado.convergiu ? "badge sucesso" : "badge"}>{resultado.convergiu ? "População convergiu" : "Limite atingido"}</span></div>
      <div className="metricas">
        <article className="metrica principal"><span>Melhor valor de x</span><strong>{resultado.x}</strong><small>candidato ótimo</small></article>
        <article className="metrica"><span>Valor de f(x)</span><strong>{resultado.aptidao.toFixed(6)}</strong><small>aptidão máxima</small></article>
        <article className="metrica"><span>Gerações</span><strong>{resultado.geracoes}</strong><small>até o critério de parada</small></article>
        <article className="metrica"><span>Cromossomo</span><strong className="mono">{resultado.cromossomo_binario}</strong><small>representação em 9 bits</small></article>
      </div>
      <div className="populacoes">
        <article><header><div><span>01</span><h3>População inicial</h3></div><small>40 indivíduos aleatórios</small></header><div className="grade-individuos">{resultado.populacao_inicial.map((item, i) => <Individuo key={`${item}-${i}`} cromossomo={item} destaque={item === melhorInicial} />)}</div></article>
        <div className="fluxo"><span>seleção</span><b>→</b><span>cruzamento</span><b>→</b><span>mutação</span></div>
        <article><header><div><span>02</span><h3>População final</h3></div><small>40 melhores sobreviventes</small></header><div className="grade-individuos">{resultado.populacao_final.map((item, i) => <Individuo key={`${item}-${i}`} cromossomo={item} destaque={item === resultado.melhor_individuo} />)}</div></article>
      </div>
    </section> : <section className="como-funciona">
      <p className="sobretitulo">COMO FUNCIONA</p><h2>Uma busca inspirada na natureza</h2>
      <div className="passos"><article><span>01</span><h3>Gerar</h3><p>Quarenta soluções aleatórias formam a população inicial.</p></article><article><span>02</span><h3>Selecionar</h3><p>A roleta favorece os candidatos com maior aptidão.</p></article><article><span>03</span><h3>Evoluir</h3><p>Cruzamento e mutação criam novas possibilidades.</p></article><article><span>04</span><h3>Sobreviver</h3><p>Os quarenta melhores avançam para a próxima geração.</p></article></div>
    </section>}
  </main>;
}

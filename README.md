# Algoritmo Genético

Aplicação acadêmica que usa um algoritmo genético em Python para encontrar o máximo global de `f(x) = x * sen(x / 20) + 100`, com `0 <= x <= 511`.

## Executar o backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python servidor.py
```

O backend ficará disponível em `http://localhost:8000`.

## Executar o frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev
```

Acesse `http://localhost:3000` e use o botão **Executar algoritmo**.

## Estrutura

- `backend/algoritmo_genetico.py`: implementação do algoritmo genético.
- `backend/servidor.py`: disponibiliza a execução para a interface.
- `frontend/`: interface Next.js para visualização dos resultados.

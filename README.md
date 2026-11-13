# ItaPede · ambiente de teste

App de delivery **fictício** de Itapeva e região, usado nas aulas de Testes de Software (SESI-SENAI Itapeva, 3º EM).
Todos os restaurantes, clientes e pedidos são dados de teste.

## Como rodar

Pré-requisitos: Python 3.10 ou mais novo e Git.

```bash
git clone <endereço do repositório>
cd itapede
python -m venv .venv
```

Ative o ambiente virtual:

- Windows (Prompt de Comando): `.venv\Scripts\activate`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Linux ou macOS: `source .venv/bin/activate`

Instale as dependências e rode:

```bash
pip install -r requirements.txt
flask --app app run --debug
```

Abra no navegador: http://127.0.0.1:5000

## Como o projeto está organizado

```
itapede/
├── app.py              rotas (telas) do app
├── regras.py           regras de negócio: pedido mínimo, taxa, cupom, quantidade
├── dados/itapede.json  "banco de dados" de teste: restaurantes, cardápios, clientes, cupons e pedidos
├── templates/          páginas HTML (Tailwind por CDN)
├── tests/              testes automatizados (pytest)
└── pytest.ini          configuração do pytest
```

## Requisitos da versão 1.3

| Código | Regra |
|---|---|
| RF01 | De 1 a 10 unidades de cada item. |
| RF02 | Pedido mínimo de R$ 20,00. De R$ 20,00 a R$ 49,99, taxa de entrega de R$ 5,00. A partir de R$ 50,00, entrega grátis. |
| RF03 | Cupom ITA15: 15% de desconto no subtotal. O pedido mínimo e a entrega grátis contam o subtotal antes do desconto. |
| RNF02 | A confirmação do pedido aparece em até 5 s. |

## Restaurante de teste

Use o **Restaurante de teste** para montar os valores dos casos de teste:

| Valor | Itens |
|---|---|
| R$ 19,99 | 1 marmitex pequeno + 1 pudim |
| R$ 20,00 | 1 marmitex pequeno + 1 refrigerante |
| R$ 35,00 | 2 marmitex pequenos + 1 refrigerante |
| R$ 40,00 | 2 marmitex pequenos + 2 refrigerantes |
| R$ 49,99 | 3 marmitex pequenos + 1 pudim |
| R$ 50,00 | 3 marmitex pequenos + 1 refrigerante |

## Testes automatizados

```bash
pip install pytest
pytest -v
```

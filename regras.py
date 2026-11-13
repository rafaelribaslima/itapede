"""Regras de negócio do ItaPede.

As funções recebem e devolvem valores em reais (por exemplo, 49.99).
Internamente, as contas são feitas em centavos para evitar erros de arredondamento.
"""

MINIMO = 2000          # RF02: pedido mínimo de R$ 20,00
TAXA = 500             # RF02: taxa de entrega de R$ 5,00
GRATIS = 5000          # RF02: entrega grátis a partir de R$ 50,00
MAX_UNIDADES = 10      # RF01: de 1 a 10 unidades de cada item
CUPONS = {"ITA15": 15}  # RF03: cupom ITA15, 15% de desconto no subtotal


def para_centavos(valor):
    return round(valor * 100)


def para_reais(centavos):
    return centavos / 100


def pode_adicionar(quantidade_atual):
    """RF01: diz se o cliente ainda pode adicionar mais uma unidade do item."""
    return quantidade_atual <= MAX_UNIDADES


def pode_finalizar(subtotal):
    """RF02: o pedido só pode ser finalizado a partir do pedido mínimo."""
    return para_centavos(subtotal) >= MINIMO


def cupom_valido(codigo):
    """RF03: diz se o código digitado é um cupom aceito."""
    return (codigo or "").strip().upper() in CUPONS


def desconto(subtotal, cupom=None):
    """RF03: valor do desconto do cupom sobre o subtotal."""
    if not cupom_valido(cupom):
        return 0.0
    percentual = CUPONS[cupom.strip().upper()]
    return para_reais(round(para_centavos(subtotal) * percentual / 100))


def taxa_entrega(subtotal, cupom=None):
    """RF02 e RF03: taxa de entrega do pedido. Devolve None abaixo do pedido mínimo."""
    if not pode_finalizar(subtotal):
        return None
    base = para_centavos(subtotal) - para_centavos(desconto(subtotal, cupom))
    return 0.0 if base >= GRATIS else para_reais(TAXA)


def total(subtotal, cupom=None):
    """Valor final: subtotal, menos o desconto, mais a taxa de entrega."""
    taxa = taxa_entrega(subtotal, cupom) or 0
    centavos = para_centavos(subtotal) - para_centavos(desconto(subtotal, cupom)) + para_centavos(taxa)
    return para_reais(centavos)


def subtotal_carrinho(itens, quantidades):
    """Soma preço × quantidade. itens: {id: preço}; quantidades: {id: quantidade}."""
    centavos = sum(para_centavos(itens[i]) * q for i, q in quantidades.items())
    return para_reais(centavos)

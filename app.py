"""ItaPede: app de delivery fictício de Itapeva e região (ambiente de teste)."""
import json
import random
import time
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for, abort

import regras

VERSAO = "1.3"
BASE = Path(__file__).parent

with open(BASE / "dados" / "itapede.json", encoding="utf-8") as arquivo:
    BANCO = json.load(arquivo)

RESTAURANTES = {r["id"]: r for r in BANCO["restaurantes"]}
PEDIDOS_NOVOS = {}
proximo_pedido = 1042

app = Flask(__name__)
app.secret_key = "itapede-ambiente-de-teste"


@app.template_filter("brl")
def brl(valor):
    return "R$ " + f"{valor:.2f}".replace(".", ",")


@app.context_processor
def dados_globais():
    return {"versao": VERSAO}


def carrinho_atual(restaurante_id):
    c = session.get("carrinho")
    if not c or c.get("restaurante_id") != restaurante_id:
        c = {"restaurante_id": restaurante_id, "itens": {}, "cupom": None}
    return c


def salvar(c):
    session["carrinho"] = c
    session.modified = True


def resumo(restaurante, c):
    precos = {str(it["id"]): it["preco"] for it in restaurante["itens"]}
    quantidades = {k: v for k, v in c["itens"].items() if v > 0}
    sub = regras.subtotal_carrinho(precos, quantidades)
    return {
        "subtotal": sub,
        "desconto": regras.desconto(sub, c["cupom"]),
        "taxa": regras.taxa_entrega(sub, c["cupom"]),
        "total": regras.total(sub, c["cupom"]),
        "pode_finalizar": regras.pode_finalizar(sub),
        "cupom": c["cupom"],
    }


def restaurante_ou_404(rid):
    r = RESTAURANTES.get(rid)
    if r is None:
        abort(404)
    return r


@app.get("/")
def inicio():
    return render_template("inicio.html", restaurantes=BANCO["restaurantes"])


@app.get("/restaurante/<int:rid>")
def restaurante(rid):
    r = restaurante_ou_404(rid)
    c = carrinho_atual(rid)
    return render_template("restaurante.html", r=r, c=c, resumo=resumo(r, c), pode_adicionar=regras.pode_adicionar)


@app.post("/restaurante/<int:rid>/adicionar/<int:item_id>")
def adicionar(rid, item_id):
    restaurante_ou_404(rid)
    c = carrinho_atual(rid)
    atual = c["itens"].get(str(item_id), 0)
    if regras.pode_adicionar(atual):
        c["itens"][str(item_id)] = atual + 1
    salvar(c)
    return redirect(url_for("restaurante", rid=rid))


@app.post("/restaurante/<int:rid>/remover/<int:item_id>")
def remover(rid, item_id):
    restaurante_ou_404(rid)
    c = carrinho_atual(rid)
    atual = c["itens"].get(str(item_id), 0)
    if atual > 0:
        c["itens"][str(item_id)] = atual - 1
    salvar(c)
    return redirect(url_for("restaurante", rid=rid))


@app.post("/restaurante/<int:rid>/cupom")
def aplicar_cupom(rid):
    restaurante_ou_404(rid)
    c = carrinho_atual(rid)
    codigo = request.form.get("cupom", "").strip().upper()
    if regras.cupom_valido(codigo):
        c["cupom"] = codigo
        flash(f"Cupom {codigo} aplicado: {regras.CUPONS[codigo]}% de desconto", "ok")
    else:
        c["cupom"] = None
        flash("Cupom inválido", "erro")
    salvar(c)
    return redirect(url_for("restaurante", rid=rid))


@app.post("/restaurante/<int:rid>/finalizar")
def finalizar(rid):
    global proximo_pedido
    r = restaurante_ou_404(rid)
    c = carrinho_atual(rid)
    res = resumo(r, c)
    if not res["pode_finalizar"]:
        flash("Pedido mínimo: R$ 20,00", "erro")
        return redirect(url_for("restaurante", rid=rid))
    time.sleep(random.uniform(2.5, 3.5))  # tempo de envio do pedido ao restaurante
    pedido = {"id": proximo_pedido, "restaurante": r["nome"], **res}
    PEDIDOS_NOVOS[proximo_pedido] = pedido
    proximo_pedido += 1
    session.pop("carrinho", None)
    return redirect(url_for("pedido", pid=pedido["id"]))


@app.get("/pedido/<int:pid>")
def pedido(pid):
    p = PEDIDOS_NOVOS.get(pid)
    if p is None:
        abort(404)
    return render_template("pedido.html", p=p)


if __name__ == "__main__":
    app.run(debug=True)

# =============================================================================
# Service — integração com https://www.espn.com.br/futebol/
# =============================================================================
#
# ---------------------------------------------------------------------------
# BIBLIOTECAS (pip install -r requirements.txt) — o que cada uma faz aqui
# ---------------------------------------------------------------------------
# flask
#   Framework da API (Blueprint, jsonify). Usado em app.py e controllers/.
#
# requests
#   Cliente HTTP — faz o GET no site do ESPN e traz o HTML (como na Aula 9).
#   Objeto importante: requests.Response ( .text, .status_code, .raise_for_status() )
#
# beautifulsoup4  (import: from bs4 import BeautifulSoup)
#   Lê HTML “bagunçado” e vira árvore de tags para buscar <a>, <h2>, etc.
#   O parser "html.parser" vem com o Python; o pacote é o BeautifulSoup.
#
# Biblioteca PADRÃO do Python (não precisa pip install):
#   re          — expressões regulares (regex); re.compile → Pattern
#   urllib.parse.urljoin — junta URL base + link relativo (/futebol/...)
#   typing      — type hints (str, list, TypedDict, etc.)
#
# ---------------------------------------------------------------------------
# TYPE HINT — hora de usar de novo (revisão da aula de tipos)
# ---------------------------------------------------------------------------
# Anotações como  nome: str  e  -> dict  NÃO convertem tipos automaticamente.
# Elas documentam o código e o editor avisa se você passar int onde esperava str.
#
# Exemplos neste arquivo:
#   modo: str                          parâmetro deve ser texto
#   -> re.Pattern[str]                 retorno é regex compilada para strings
#   vistos: set[tuple[str, str | None]] conjunto de tuplas (texto, url ou None)
#   mencoes: list[dict]                lista de dicionários
#   -> ResultadoBusca                  TypedDict — dict com chaves conhecidas
#
# str | None  significa “str ou None” (equivalente antigo: Optional[str]).
#
# ---------------------------------------------------------------------------
# O que é re.Pattern
# ---------------------------------------------------------------------------
# re.compile(r"brasileir[aã]o") NÃO devolve string — devolve um Pattern:
#   um objeto regex JÁ COMPILADO, pronto para .search(texto), .match(...), etc.
#
# Por que compilar antes do loop?
#   Compilar uma vez e reutilizar em milhares de títulos é mais rápido
#   do que recompilar a expressão a cada linha.
#
# re.Pattern[str] no type hint = “Pattern que trabalha com str” (Python 3.9+).
# =============================================================================

from __future__ import annotations

import re
from typing import TypedDict
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Página inicial de futebol do ESPN — o conteúdo muda ao longo do dia (notícias ao vivo).
URL_GE: str = "https://www.espn.com.br/futebol/"

# Evita travar para sempre se o site não responder.
TIMEOUT: int = 15

# Alguns sites bloqueiam User-Agent vazio; identificamos o cliente educacional.
USER_AGENT: str = "Mozilla/5.0 (compatible; TecTI-Aula16/1.0; +aula-educacional)"

# Expressões regulares para achar "Brasileirão" (com ou sem til, maiúsc/minúsc).
# re.compile → re.Pattern[str]  (objeto regex, não string).
REGEX_SUBSTRING: re.Pattern[str] = re.compile(r"brasileir[aã]o", re.IGNORECASE)

# \b = limite de palavra — evita casar pedaços estranhos em palavras longas.
REGEX_PALAVRA: re.Pattern[str] = re.compile(r"\bbrasileir[aã]o\b", re.IGNORECASE)


class Mencao(TypedDict):
    """Formato de UMA menção no JSON — TypedDict ajuda o type checker."""

    texto: str
    trecho: str
    url: str | None
    tag: str


class ResultadoBusca(TypedDict):
    """Formato completo retornado por buscar_mencoes_selecao()."""

    fonte: str
    termo_busca: str
    modo_busca: str
    total: int
    mencoes: list[Mencao]


def _padrao_busca(modo: str) -> re.Pattern[str]:
    """Escolhe qual regex (Pattern) usar conforme o parâmetro ?modo= da API."""
    if modo == "palavra":
        return REGEX_PALAVRA
    return REGEX_SUBSTRING


def _trecho_com_destaque(
    texto: str,
    padrao: re.Pattern[str],
    janela: int = 60,
) -> str:
    """
    Recorta um pedaço do texto em torno da primeira ocorrência de 'Brasileirão'.
    padrao.search(texto) usa o Pattern compilado — retorna Match ou None.
    """
    match = padrao.search(texto)
    if not match:
        return texto[:120]

    inicio = max(0, match.start() - janela // 2)
    fim = min(len(texto), match.end() + janela // 2)
    trecho = texto[inicio:fim].strip()

    if inicio > 0:
        trecho = "…" + trecho
    if fim < len(texto):
        trecho = trecho + "…"
    return trecho


def buscar_mencoes_selecao(modo: str = "substring") -> ResultadoBusca:
    """
    Função principal do Service — chamada pelo Controller.

    modo:
      - "substring": qualquer texto que contenha brasileirão/brasileirao
      - "palavra": só quando 'Brasileirão' aparece como palavra isolada
    """
    padrao: re.Pattern[str] = _padrao_busca(modo)

    try:
        resposta: requests.Response = requests.get(
            URL_GE,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        resposta.raise_for_status()
    except requests.RequestException as erro:
        raise ConnectionError(f"Não foi possível acessar o ESPN: {erro}") from erro

    resposta.encoding = resposta.apparent_encoding or "utf-8"

    soup = BeautifulSoup(resposta.text, "html.parser")

    vistos: set[tuple[str, str | None]] = set()
    mencoes: list[Mencao] = []

    for tag in soup.find_all(["a", "h1", "h2", "h3", "h4", "p", "span"]):
        texto = tag.get_text(" ", strip=True)

        if not texto or not padrao.search(texto):
            continue
        if len(texto) < 3:
            continue

        url: str | None = None
        if tag.name == "a" and tag.get("href"):
            url = urljoin(URL_GE, tag["href"])

        chave = (texto[:200], url)
        if chave in vistos:
            continue
        vistos.add(chave)

        mencoes.append(
            Mencao(
                texto=texto,
                trecho=_trecho_com_destaque(texto, padrao),
                url=url,
                tag=tag.name,
            )
        )

    return ResultadoBusca(
        fonte=URL_GE,
        termo_busca="Brasileirão",
        modo_busca=modo,
        total=len(mencoes),
        mencoes=mencoes,
    )

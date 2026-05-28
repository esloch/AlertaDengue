from __future__ import annotations

from typing import Any

from django.templatetags.static import static
from django.utils.translation import gettext as _


def member(
    name: str,
    role: str,
    photo: str | None = None,
    href: str | None = None,
) -> dict[str, str]:
    data = {"name": name, "role": role}
    if photo:
        data["photo"] = static(photo)
    if href:
        data["href"] = href
    return data


def link_item(
    label: str,
    href: str | None = None,
    text: str | None = None,
    children: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    data: dict[str, Any] = {"label": label}
    if href:
        data["href"] = href
    if text:
        data["text"] = text
    if children:
        data["children"] = children
    return data


def get_team_page_props() -> dict[str, Any]:
    return {
        "hero": {
            "title": _("Quem faz o Infodengue"),
            "body": _(
                "O Infodengue, fruto de uma articulação entre a Fiocruz e "
                "Emap/FVG, é um sistema criado e desenvolvido por "
                "pesquisadores de instituições públicas e privadas que "
                "buscam soluções para o monitoramento de doenças "
                "transmitidas por vetores. Nossa equipe é composta por uma "
                "rede multidisciplinar que engloba profissionais da saúde, "
                "da tecnologia de informação, ciência de dados, vigilância "
                "epidemiológica e comunicação."
            ),
        },
        "sections": [
            {
                "kind": "members",
                "title": _("Coordenação Geral"),
                "members": [
                    member(
                        "Cláudia Torres Codeço",
                        _("PROCC/Fiocruz"),
                        "img/team/claudia.png",
                        "https://lattes.cnpq.br/1929576902623348",
                    ),
                    member(
                        "Flávio Codeço Coelho",
                        _("Escola de Matemática Aplicada/FGV"),
                        "img/team/flavio.jpg",
                        "https://lattes.cnpq.br/0309050626285266",
                    ),
                    member(
                        "Leonardo Soares Bastos",
                        _("PROCC/Fiocruz"),
                        "img/team/leo.jpg",
                        "https://lattes.cnpq.br/5241799121437269",
                    ),
                    member(
                        "Oswaldo Gonçalves Cruz",
                        _("PROCC/Fiocruz"),
                        "img/team/oswaldo.png",
                        "https://lattes.cnpq.br/9530671289607786",
                    ),
                ],
            },
            {
                "kind": "members",
                "title": _("Dados e situação epidemiológica"),
                "members": [
                    member(
                        "Sara de Souza Oliveira",
                        _("Analista Infodengue - epidemiologia"),
                        "img/team/sara.jpg",
                        "https://lattes.cnpq.br/2864482261450215",
                    ),
                    member(
                        "Thais I S Riback",
                        _("Analista Infodengue - epidemiologia"),
                        "img/team/thais.jpg",
                        "https://lattes.cnpq.br/4335590727747384",
                    ),
                    member(
                        "Vinicius Godinho",
                        _("Analista Infodengue - ciência de dados"),
                        "img/team/vinicius.jpg",
                        "https://lattes.cnpq.br/8508944359245527",
                    ),
                    member(
                        "Eduardo Correa Araujo",
                        _("Analista Infodengue - ciência de dados"),
                        "img/team/eduardo.jpg",
                        "https://lattes.cnpq.br/2326164285897270",
                    ),
                ],
            },
            {
                "kind": "members",
                "title": _("Desenvolvimento"),
                "members": [
                    member(
                        "Luã Bida Vacaro",
                        _("TI Infodengue & Mosqlimate"),
                        "img/team/lua.jpeg",
                        "https://lattes.cnpq.br/2917646970654963",
                    ),
                    member(
                        "Sandro Loch",
                        _("Platform & Data Infrastructure Engineer"),
                        "img/team/sandro.jpeg",
                        "https://esloch.github.io/cv/",
                    ),
                ],
            },
            {
                "kind": "members",
                "title": _("Pesquisa, comunicação e formação"),
                "members": [
                    member(
                        "Raquel Martins Lana",
                        _(
                            "Pesquisadora associada - Barcelona "
                            "Supercomputing Center (BSC) - Espanha"
                        ),
                        "img/team/raquel.jpg",
                        "https://lattes.cnpq.br/2518752229392005",
                    ),
                    member(
                        "Laís Picinini Freitas",
                        _("Pesquisadora associada - PROCC/Fiocruz"),
                        "img/team/lais.png",
                        "https://lattes.cnpq.br/2996805485281003",
                    ),
                    member(
                        "Iasmim Ferreira de Almeida",
                        _("Pesquisadora associada - Emap/FGV"),
                        "img/team/iasmim.jpg",
                        "https://lattes.cnpq.br/6555136792794111",
                    ),
                    member(
                        "Ramila Alencar",
                        _(
                            "Programa de Doutorado em Epidemiologia em "
                            "Saúde Pública - ENSP/Fiocruz"
                        ),
                        "img/team/ramila.webp",
                        "https://lattes.cnpq.br/0485886911362331",
                    ),
                    member(
                        "Ayrton Gouveia",
                        _(
                            "Programa de Doutorado em Epidemiologia em "
                            "Saúde Pública - ENSP/Fiocruz"
                        ),
                        "img/team/ayrton.jpeg",
                        "https://lattes.cnpq.br/2651948797512226",
                    ),
                    member(
                        "Nathaly Dutra",
                        _(
                            "Doutoranda no Programa de Epidemiologia e "
                            "Saúde Pública da ENSP"
                        ),
                        "img/team/nathaly.jpeg",
                    ),
                    member(
                        "Danielle Andreza da Cruz Ferreira",
                        _("Pesquisadora associada - UFMG"),
                        "img/team/danielle.jpg",
                        "https://lattes.cnpq.br/0421717413079286",
                    ),
                ],
            },
            {
                "kind": "list",
                "title": _("Comunidade Infodengue"),
                "intro": _(
                    "Agradecemos a todos que participaram da comunidade "
                    "Infodengue."
                ),
                "items": [
                    link_item(
                        "Marcelle Chagas",
                        "https://lattes.cnpq.br/2219603304725763",
                        _("Comunicação e engajamento"),
                    ),
                    link_item(
                        "Ivan Ogasawara",
                        "https://lattes.cnpq.br/7764277601641080",
                        _("Consultor externo"),
                    ),
                    link_item(
                        "Lucas Monteiro Bianchi",
                        "https://lattes.cnpq.br/5099258319176445",
                        _("Analista de dados"),
                    ),
                    link_item(
                        "Mauro Martins Teixeira",
                        "https://lattes.cnpq.br/1316412551645220",
                        _("Observatório da Dengue/UFMG"),
                    ),
                    link_item(
                        "Magda C V C Ribeiro",
                        "https://lattes.cnpq.br/5566477869758674",
                        _("Instituto de Biociências/UFPR"),
                    ),
                    link_item(
                        "Marcelo F C Gomes",
                        "https://lattes.cnpq.br/6064559192125515",
                        _("PROCC/Fiocruz"),
                    ),
                    link_item(
                        "Daniel A M Villela",
                        "https://lattes.cnpq.br/4016632420686251",
                        _("PROCC/Fiocruz"),
                    ),
                    link_item(
                        "Marcelo F C Gomes",
                        "https://lattes.cnpq.br/6064559192125515",
                        _("IOC/Fiocruz"),
                    ),
                    link_item(
                        "Dalila Oliveira",
                        "https://lattes.cnpq.br/6064559192125515",
                        _(
                            "Programa de Mestrado em Medicina Tropical - "
                            "IOC/Fiocruz"
                        ),
                    ),
                    link_item(
                        "Jo de Napole Arruda Dias",
                        "https://lattes.cnpq.br/6064559192125515",
                        _(
                            "Programa de Mestrado em Biologia Computacional "
                            "e Sistemas - IOC/Fiocruz"
                        ),
                    ),
                ],
            },
            {
                "kind": "list",
                "title": _("Parcerias"),
                "intro": _(
                    "O Infodengue mantém colaborações estratégicas e atua "
                    "como parte interessada em outros projetos e programas, "
                    "promovendo trocas e parcerias. Entre eles estão:"
                ),
                "listClassName": "team-partnerships-list",
                "items": [
                    link_item(
                        _(
                            "Coordenação-Geral de Vigilância de Arboviroses "
                            "- Ministério da Saúde (CGArb)"
                        ),
                        (
                            "https://www.gov.br/saude/pt-br/centrais-de-"
                            "conteudo/publicacoes/guias-e-manuais/2025/"
                            "plano-de-contingencia-nacional-para-dengue-"
                            "chikungunya-e-zika.pdf"
                        ),
                        _(
                            "Plano de Contingência Nacional para Dengue, "
                            "Chikungunya e Zika (documento que define as "
                            "modelagens encomendadas ao infodengue como uma "
                            "das estratégias para subsidiar a tomada de "
                            "decisão na preparação para epidemias por "
                            "arboviroses)."
                        ),
                    ),
                    link_item(
                        _("Organização Pan-Americana da Saúde (OPAS/OMS)"),
                        "https://www.paho.org/pt/brasil",
                    ),
                    link_item(
                        "Mosqlimate",
                        "https://mosqlimate.org/",
                        _(
                            "Intelligent Surveillance of Arboviruses and Climate"
                        ),
                    ),
                    link_item(
                        _("Barcelona Supercomputing Center (BSC)"),
                        "https://www.bsc.es/",
                        children=[
                            link_item(
                                "HARMONIZE",
                                (
                                    "https://www.bsc.es/research-and-"
                                    "development/projects/harmonize-"
                                    "harmonizing-multi-scale-spatiotemporal-"
                                    "data-health"
                                ),
                                _(
                                    "Harmonizing multi-scale spatiotemporal "
                                    "data for health in climate."
                                ),
                            ),
                            link_item(
                                "IDExtremes",
                                (
                                    "https://www.bsc.es/es/research-and-"
                                    "development/projects/idextremes-digital-"
                                    "technology-development-award-climate-"
                                    "sensitive"
                                ),
                                _(
                                    "Digital Technology Development Award in "
                                    "Climate Sensitive Infectious Disease "
                                    "Modelling."
                                ),
                            ),
                        ],
                    ),
                    link_item(
                        _(
                            "The Global Health Network Latin America and "
                            "Caribbean (TGHN LAC)"
                        ),
                        "https://lac.tghn.org/projetos-pathfinder/infodengue/",
                    ),
                ],
            },
            {
                "kind": "list",
                "title": _("Apoio"),
                "items": [
                    link_item(_("DECIT/MS (2014-2016)")),
                    link_item(_("Fiocruz Edital Inova 2019 (2019-2021)")),
                    link_item(_("FNS/MS (2020-2027)")),
                ],
            },
        ],
        "contact": {
            "prompt": _(
                "Gostaria de ter mais informações ou tirar dúvidas sobre o "
                "Sistema de Alerta Infodengue?"
            ),
            "label": _("Entre em contato conosco"),
            "href": "mailto:alerta_dengue@fiocruz.br",
        },
    }

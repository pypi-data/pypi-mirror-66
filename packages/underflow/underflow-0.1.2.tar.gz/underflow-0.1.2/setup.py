# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['underflow']

package_data = \
{'': ['*']}

install_requires = \
['click-spinner>=0.1.8,<0.2.0',
 'dacite>=1.4.0,<2.0.0',
 'fastapi>=0.54.1,<0.55.0',
 'httpx>=0.12.1,<0.13.0',
 'pydantic[dotenv]>=1.4,<2.0',
 'python-telegram-bot>=12.6.1,<13.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'typer>=0.1.1,<0.2.0',
 'uvicorn>=0.11.3,<0.12.0']

entry_points = \
{'console_scripts': ['underflow = underflow.cli:app']}

setup_kwargs = {
    'name': 'underflow',
    'version': '0.1.2',
    'description': 'Pesquisas do stackoverflow via cli',
    'long_description': 'Underflow\n=========\n:License: GPLv3\n\n\nPesquisa no StackOverflow\n-------------------------\n\nEste projeto disponibiliza um comando CLI que coordena ações com o objetivo\nde realizar pesquisa no StackOverflow, possui 2 interfaces de uso:\n\n  * Pesquisas por CLI\n  * Pesquisas por Bot Telegram\n\n\nArquitetura do projeto\n----------------------\n\nO Projeto está dividido hein:\n\n  * API de Comunicação com StackOverflow\n  \n    * Executa pesquisa na API;\n    * Executa paginação preemptiva\n    * Captura token de autenticação com a API do Stack OverFlow (Para permitir maior quota de requisições)\n    \n  * CLI de interação com a API de Comunicação\n  \n    * Interage com a API interna de comunicação\n    * Redireciona requisição de autenticação OAuth pro StackOverFlow, modo implicito.\n    \n  * Bot Server\n  \n    * Responde as solicitações de pessoas interagindo com o bot\n\n\nPré-requisitos\n--------------\n\nAntes de qualquer interação de pesquisa, você precisa iniciar a API de comunicação com o StackOverflow.\n\nPortanto abra um novo terminal e execute:\n\n  $ underflow start-api\n\nPesquisas via CLI\n^^^^^^^^^^^^^^^^^\n\nÉ permitido o uso da CLI sem pre-requisitos de autenticação.\n\n  $ underflow ask "python + fastapi"\n\n\nAuthenticação\n^^^^^^^^^^^^^\n\nExiste um limite de requisições. Caso necessite de autenticação, será preciso que você se autentique e\nautorize este aplicativo a realizar pesquisas.\n\nPara viabilizar essa autenticação é necessário algumas informações sensíveis que podem\nser obtidas com o author deste projeto. De posse dessas informações,\ncoloque as informações como variaveis de ambiente e siga os passos.\n\nApós inserir, você pode executar o comando de autenticação:\n\n  $ underflow authenticate\n\nO comando abrirá o Google Chrome, redirecionando você para mecanismo de autenticação e autorização do StackOverflow,\numa vez autorizado, você será redirecionado para uma página localhost para que a API interna possa capturar o token e\nsalvar em memória. Após isso pode continuar realizando as consultas.\n\n\n\nTelegram BOT\n^^^^^^^^^^^^\n\nO nome do bot no Telegram é UnderflowBot. Para responder as solicitações oriundas do bot, você precisa de algumas\ninformações secretas de integração, solicitar para o author. De posse dessa informações, voce exporta para variaveis\nde ambiente e executar o comando abaixo para responder as solicitações.\n\n  $ underflow bot-server\n\n\nDesenvolvimento\n---------------\n\nProjeto foi desenvolvido principalemente com poetry + fastapi + typer + pytest, as demais dependências são utilitários.\n\n\n\nInstalaçao de dependências\n--------------------------\n\n  $ poetry install \n\n\nTestes\n------\n\n  $ poetry run pytest\n\n\n\nPossível Roadmap Futuro\n-----------------------\n\n  * Desenvolvedor botserver em arquitetura serverless(aws lambda)\n  * Implementar autenticação entre as camadas\n  * Implementar controle de background e foreground\n  * Implementar respostas interativas para o bot do Telegram\n',
    'author': 'Daniel Santos',
    'author_email': 'daniel.martins@lumedigital.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielmartins/underflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

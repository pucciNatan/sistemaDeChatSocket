# Sistema de Chat Socket
Um projeto desenvolvido usando Python + Socket onde o usuário loga no sistema, informa seu nome e a sala que deseja entrar, sendo possível conversar com outros usuários presentes na mesma sala.

1. Clone o repositório para a sua máquina e verifique se o Python está instalado.
2. Para rodar o programa, navegue até a pasta `server` no terminal, depois rode primeiramente o servidor usando `python servidor.py`.
3. Abra um novo terminal e rode `python cliente.py`, informe o nome do cliente, o nome da sala que deseja entrar e aparecerá um chat.
4. Novamente, abra um novo terminal, navegue até a pasta `server` e rode `python cliente.py` para criar um novo cliente. 
5. Informe o nome desse novo cliente, a sala que ele deseja entrar (coloque o mesmo nome da sala do cliente anterior) e será possível faze-los conversarem.
6. Repita o processo 4 e 5 quantas vezes você quiser e faça muitos clientes da mesma sala conversarem entre si.

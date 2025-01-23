<div align="center">
    <img src="https://github.com/user-attachments/assets/b7d9a629-d340-4ba2-a8a5-23d42164b364" alt="Minha Imagem" width="500"/>
</div>

# Arquitetura do case
<div align="center">
    <img src="https://github.com/user-attachments/assets/4e7a2757-7c4d-4d60-a455-4e20c98b1a7c" alt="Minha Imagem" width="500"/>
</div>

## Dependências do projeto

- **WSL** com WSL instalado
- **Python 3.9 ou superior** - Versão usada 3.12
- **Java 8 ou superior** - Versão usada JDK 21
- **Spark 3.4 ou superior** - Versão usada 3.5.3
- **AirFlow 2.7 ou superior** - Versão usada 2.10.2
- **Delta-spark**

# Configurando WSL

Este guia fornece um passo a passo para configurar e executar o case em um ambiente Windows Subsystem for Linux (WSL).

## Passo a Passo

### 1. Instalar o WSL

Se você ainda não tem o WSL instalado, siga estes passos:

- Abra o PowerShell como Administrador e execute:
  ```bash
  wsl --install
  
### 2. Escolher uma distro Linux
Após a instalação do WSL, escolha uma distribuição de sua preferência, no meu caso utilizei o Ubuntu. A instalação da distribuição é a partir da Microsoft Store.

### 3. Configurar o Ambiente WSL
- Abra o WSL e atualize os pacotes:
   ```bash
   sudo apt update && sudo apt upgrade -y

- Instale o Python:
   ```bash
   sudo apt install python3

- Instale o Java (JDK):
  ```bash
  sudo apt install default-jdk
Obs: será preciso inserir a senha que você definiu para seguir essa etapa.

- Espere o download ser realizado e ao final utilize esse comando para verificar a instalação:
  ```bash
  java --version

- Instalando o Spark
Para instalar o Apache Spark será necessário mudar para o usuário root, então utilize esse comando:
    ```bash
    sudo su
    
- Em seguida será preciso criar um diretório para o spark, então rode o seguinte comando:
    ```bash
    mkdir -p /opt/spark
    cd /opt/spark

Acesse [akafa](https://spark.apache.org/downloads.html) e selecione a versão desejada do Apache Spark (em vermelho). Em seguida clique no link apresentado (em preto):
<div align="center">
    <img src="https://github.com/user-attachments/assets/2e0cbb2f-f3cb-4a71-9daa-aa0b9b09f287" alt="Minha Imagem" width="500"/>
</div>

Você será redirecionado para outra página. Copie qualquer um dos links (em vermelho):
<div align="center">
    <img src="https://github.com/user-attachments/assets/7a91d9b3-e7e8-4b99-bb20-9728e6e2f201" alt="Minha Imagem" width="500"/>
</div>

No meu caso utilizei a versão **3.5.3 do Apache Spark**, substitua o necessário conforme a versão que foi baixada.

- Voltando ao seu terminal utilize o seguinte comando:
    ```bash
    wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz

- Espere o download ocorrer e então rode o seguinte comando para descompactar o arquivo:
    ```bash
    tar -xvf spark-3.5.3-bin-hadoop3.tgz

- Com tudo descompactado agora é preciso definir o Spark como variável de ambiente:
  ```bash
  cd
  vi .bashrc
Obs: 
1. O cd sem caminho irá redirecionar para o diretório base do usuário root.
2. O .bashrc é um arquivo de configuração da distro, iremos fazer uma alteração nele.

- Ao abrir o arquivo navegue até o final dele, em seguida pressione 'i' no teclado para liberar a escrita no arquivo. Digite o seguinte:
<div align="center">
    <img src="https://github.com/user-attachments/assets/815f66e6-9e5e-4634-8443-8aa2fb7ff1d3" alt="Minha Imagem" width="500"/>
</div>
Para finalizar a escrita clique em 'Esc' no teclado e digite ':wq' e aperte o Enter.

Tendo realizado todos os passos corretamente será possível iniciar o spark em sua máquina:
<div align="center">
    <img src="https://github.com/user-attachments/assets/6181cb32-c936-4e77-bc82-3fdaa7959135" alt="Minha Imagem" width="500"/>
</div>
Para sair do spark sheel pressione CTRL + D

### 4. Criando ambiente virtual
- Agora que realizamos as configurações necessárias no WSL, temos que criar um ambiente virtual e ativá-lo:
    ```bash
    python3 -m venv airflow_venv
    source airflow_venv/bin/activate

- Faça a instalação do Delta, padrão de arquivo utilizado pelos scripts Python de ETL desenvolvidos nesse case:
  ```bash
  pip install delta-spark
Automaticamente a versão compatível com o Spark será instalada.
    
- Em seguida iremos instalar o AirFlow, para isso é preciso especificar a versão do Python utilizada e a versão do AirFlow compatível:
    ```bash
    pip install "apache-airflow==2.10.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.12.txt"

- Agora precisamos criar um usuário para acessar o Airflow, então inicie o database:
  ```bash
  airflow db init

- Por fim substitua as informações necessárias para rodar o comando abaixo:
  ```bash
  airflow users create -u USERNAME -f FIRST_NAME -l LAST_NAME -r Role(Existem Admin, User, Viewer, Op, Public) -e EMAIL -p PASSWORD

- Agora inicie o Web Server:
  ```bash
  airflow webserver --port 8080
  
- Abra uma novo terminal ative o ambiente virtual e inicie o Scheduler:
  ```bash
  airflow webserver --port 8080

O Web Server é a interface para interagir com o AirFlow, enquanto o Scheduler por executar as DAGs conforme a orquestração e horário definido.

Se os passos foram seguidos o AirFlow está operante. Para confirmar abra algum navegador na sua máquina e acessar o localhost:8080 (ou a porta que você especificou), assim você acessar o Web Server do AirFlow para visualizar as DAGs.
Quando quiser parar o AirFlow basta apertar CTRL + C em ambos os terminais.

### 5. Usando scripts desenvolvidos
Dentro da pasta src neste repositório existe outros dois diretórios:
    - dags | Contém a DAG que faz a orquestração dos códigos
    - pipelines | Scripts Python desenvolvidos para a ingestão, tratamento e escrita dos dados.

A pasta de dags precisara ser colocada dentro da pasta airflow, que foi criada automaticamente ao rodar o pip install. Ela por padrão é criada fora da venv para armazenar dados persistentes.
A pasta de pipelines precisara ser colocada dentro da pasta do ambiente virtual.

**Será necessário modificar os seguintes caminhos nos arquivos:***
- ingestion_breweries
- transform_breweries
- analytics_breweries
- brewerie_dag

As modificações serão somente com relação ao caminho dos arquivos que serão escritos/lidos, pois isso vai variar com o nome do usuário do WSL e das pastas criadas.
A DAG está configurada para ser executada uma vez ao dia às 15:30 (UTC-03:00).

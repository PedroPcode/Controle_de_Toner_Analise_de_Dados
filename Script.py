import pyodbc
from datetime import datetime, timedelta
import random
import string

# Configurações do SQL Server
server = 'DESKTOP-IMP5BJA' 
database = 'Controle_de_Toner'

conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Modelos de impressoras
impressoras_modelos = {
    'SL-M4080FX': {'fabricante': 'Samsung', 'toners': {'preto': 'MLT-D201L', 'ciano': None, 'magenta': None, 'amarelo': None}},
    'SL-K4250RX': {'fabricante': 'Samsung', 'toners': {'preto': 'MLT-D708L', 'ciano': None, 'magenta': None, 'amarelo': None}},
    'SL-C4062FX': {'fabricante': 'Samsung', 'toners': {'preto': 'CLT-K603L', 'ciano': 'CLT-C603L', 'magenta': 'CLT-M603L', 'amarelo': 'CLT-Y603L'}},
    'SL-X4220RX': {'fabricante': 'Samsung', 'toners': {'preto': 'CLT-K808S', 'ciano': 'CLT-C808S', 'magenta': 'CLT-M808S', 'amarelo': 'CLT-Y808S'}}
}

clientes_ficticios = [
    'AlphaTech', 'BetaCorp', 'Gamma Solutions', 'DeltaWorks', 'Epsilon Ltda',
    'Zeta Industries', 'Eta Services', 'Theta Enterprises', 'Iota Systems', 'Kappa Group'
]

locais_empresa = [
    'Administrativo', 'Estoque', 'Recepção', 'Financeiro', 'TI',
    'Comercial', 'RH', 'Marketing', 'Manutenção', 'Diretoria',
    'Contabilidade', 'Suporte Técnico', 'Logística', 'Expedição',
    'Almoxarifado', 'Copa', 'Auditoria', 'Qualidade', 'Engenharia',
    'Vendas', 'Secretaria', 'Juridico', 'Planejamento', 'Produção',
    'Pesquisa e Desenvolvimento', 'SAC', 'Controladoria', 'Compras',
    'Arquivos', 'Tesouraria', 'Patrimônio', 'Estacionamento',
    'Sala de Reunião 1', 'Sala de Reunião 2', 'Sala de Treinamento',
    'Biblioteca', 'Auditório', 'Cafeteria', 'Pátio', 'Recepção 2',
    'Prédio 1', 'Prédio 2', 'Prédio 3', 'Piso 1', 'Piso 2',
    'Câmera Fria', 'Área Externa', 'Portaria', 'Sala VIP',
    'Atendimento', 'Help Desk', 'Laboratório', 'Departamento Pessoal',
    'TI Backup', 'Data Center', 'Cofre', 'Estacionamento Visitantes',
    'Área Técnica', 'Gerência', 'Coordenação', 'Secretaria Executiva'
]

def gerar_porcentagem():
    return random.randint(0, 100)

def gerar_dias_restantes():
    return str(random.randint(1, 100))

def gerar_serie_unica(cursor):
    while True:
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        numeros = ''.join(random.choices(string.digits, k=5))
        serie = letras + numeros
        cursor.execute("SELECT COUNT(*) FROM monitoramento WHERE serie = ?", (serie,))
        if cursor.fetchone()[0] == 0:
            return serie

def gerar_ip_unico(cursor):
    while True:
        parte1 = random.randint(100, 999)
        parte2 = random.randint(0, 99)
        ip = f"10{parte1}.{parte2:02d}"
        cursor.execute("SELECT COUNT(*) FROM monitoramento WHERE endereco_ip = ?", (ip,))
        if cursor.fetchone()[0] == 0:
            return ip

def gerar_apelido_aleatorio():
    local = random.choice(locais_empresa)
    numero = random.randint(100, 299)
    return f"{local} {numero}"

# Sorteia de 1 a 5 índices que terão data_monitoramento diferente do dia atual (defasados)
quantidade_defasadas = random.randint(1, 5)
indices_defasados = random.sample(range(20), quantidade_defasadas)

print(f"Quantidade de impressoras sem monitoramento hoje: {quantidade_defasadas}")
print(f"Índices com status 'Sem monitoramento': {indices_defasados}")

# Inserir 20 impressoras
for i in range(20):
    modelo_imp = random.choice(list(impressoras_modelos.keys()))
    fabricante = impressoras_modelos[modelo_imp]['fabricante']
    toners = impressoras_modelos[modelo_imp]['toners']

    serie = gerar_serie_unica(cursor)
    endereco_ip = gerar_ip_unico(cursor)
    apelido = gerar_apelido_aleatorio()
    cliente = random.choice(clientes_ficticios)

    data_coleta = datetime.now()

    # data_monitoramento: para defasados, dias atrás; para os demais, igual data_coleta
    if i in indices_defasados:
        dias_atras = random.randint(1, 5)
        data_monitoramento = data_coleta - timedelta(days=dias_atras)
    else:
        data_monitoramento = data_coleta

    status_monitoramento = 'Monitorando' if data_monitoramento.date() == data_coleta.date() else 'Sem monitoramento'

    preto_percent = gerar_porcentagem()
    dias_restantes_preto = gerar_dias_restantes()
    modelo_toner_preto = toners['preto']

    if toners['ciano']:
        ciano_percent = gerar_porcentagem()
        dias_restantes_ciano = gerar_dias_restantes()
        modelo_toner_ciano = toners['ciano']
    else:
        ciano_percent = dias_restantes_ciano = modelo_toner_ciano = None

    if toners['magenta']:
        magenta_percent = gerar_porcentagem()
        dias_restantes_magenta = gerar_dias_restantes()
        modelo_toner_magenta = toners['magenta']
    else:
        magenta_percent = dias_restantes_magenta = modelo_toner_magenta = None

    if toners['amarelo']:
        amarelo_percent = gerar_porcentagem()
        dias_restantes_amarelo = gerar_dias_restantes()
        modelo_toner_amarelo = toners['amarelo']
    else:
        amarelo_percent = dias_restantes_amarelo = modelo_toner_amarelo = None

    cursor.execute("""
        INSERT INTO monitoramento (
            serie, endereco_ip, apelido, fabricante, modelo, cliente,
            data_coleta, data_monitoramento,
            preto_percent, dias_restantes_preto, modelo_toner_preto,
            ciano_percent, dias_restantes_ciano, modelo_toner_ciano,
            magenta_percent, dias_restantes_magenta, modelo_toner_magenta,
            amarelo_percent, dias_restantes_amarelo, modelo_toner_amarelo,
            status_monitoramento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        serie, endereco_ip, apelido, fabricante, modelo_imp, cliente,
        data_coleta, data_monitoramento,
        preto_percent, dias_restantes_preto, modelo_toner_preto,
        ciano_percent, dias_restantes_ciano, modelo_toner_ciano,
        magenta_percent, dias_restantes_magenta, modelo_toner_magenta,
        amarelo_percent, dias_restantes_amarelo, modelo_toner_amarelo,
        status_monitoramento
    ))

conn.commit()
conn.close()

print(f"✅ Impressoras inseridas com sucesso! {quantidade_defasadas} estão com status 'Sem monitoramento'.")

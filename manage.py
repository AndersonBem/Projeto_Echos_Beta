#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import shutil  # Importando o módulo shutil


backup_already_done = False  # Variável para rastrear se o backup já foi feito

def make_backup():
    """
    Faz o backup do banco de dados PostgreSQL.
    """
    global backup_already_done

    if backup_already_done:
        return

    load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
    db_password = os.getenv('PASSWORD')

    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backup')
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql")

    # Segundo diretório de backup
    backup_dir2 = r'C:\Empresa\Backup\Sistema_eccos\Backup_sistema'
    os.makedirs(backup_dir2, exist_ok=True)
    backup_file2 = os.path.join(backup_dir2, f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql")

    
    
    # Caminho completo para o pg_dump
    pg_dump_path = r'C:\Program Files\PostgreSQL\16\bin\pg_dump.exe'  # Substitua pelo caminho correto
    
    command = [
        pg_dump_path,
        '-U', 'postgres',  # Altere isso se o nome de usuário for diferente
        '-h', 'localhost',
        '-p', '5432',
        '-F', 'c',  # Formato de backup personalizado do PostgreSQL
        '-f', backup_file,
        'Projeto Echos'  # Nome do banco de dados
    ]
    # Adicione a senha como uma variável de ambiente
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    subprocess.run(command, env=env)

    # Copia o backup para o segundo diretório
    shutil.copy(backup_file, backup_file2)
    
    backup_already_done = True  # Marca o backup como já feito

    print("Backup concluído com sucesso!")
    print(f"Arquivo de backup criado em: {backup_file}")
    print(f"Arquivo de backup copiado para: {backup_file2}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Faz o backup antes de executar outros comandos
    if 'runserver' in sys.argv:
        make_backup()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

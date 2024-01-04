import subprocess
import os

def runCommand(command):
  result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  if result.returncode == 0:
    print("Command executed successfully:")
    print(result.stdout)
  else:
    print("Error executing the command:")
    print(result.stderr)

script_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.abspath(os.path.join(script_dir, '../../'))
runCommand(f'cd {destination_dir} && source ./venv/bin/activate && cd scrap_detik/scrap_detik && scrapy crawl sindonews')




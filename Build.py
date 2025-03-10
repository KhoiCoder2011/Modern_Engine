import os
import time
import File as file
import shutil
import subprocess

start = time.time()

os.system('cls' if os.name == 'nt' else 'clear')

script_name = 'Engine'
shader_name = 'shader'
glfw_lib_path = 'glfwlib\glfw3.dll'

print('Engine Build Tool.')

# os.system('pip install pyinstaller')

print('-------------------------')

if os.path.exists('dist'):
    shutil.rmtree('dist')

os.system(f'''pyinstaller --onefile\
          --add-data "{glfw_lib_path};."\
          {script_name}.py
''')

file.copy_folder('assets', 'dist/assets')
file.copy_folder('Font', 'dist/Font')
file.copy_folder('shaders', 'dist/shaders')
file.copy_folder('Config', 'dist/Config')

end = time.time()

print(f"Time elapsed: {end - start} seconds")

print('Run the executable file in the dist folder')

if input('Run file (y/n): ') == 'y':
    subprocess.run([f'dist/{script_name}.exe'])

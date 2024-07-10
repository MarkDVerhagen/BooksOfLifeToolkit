import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python3', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

def main():
    print("Running main.py")
    
    # List of scripts to run
    scripts = ['synth/gen_rin_hashes.py', 'synth/householdbus.py',
               'synth/persoontab.py', 'synth/vektistab.py']
    
    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
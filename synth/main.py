def main():
    print("Running main.py")
    
    # List of scripts to run
    scripts = ['gen_rin_hashes', 'householdbus',
               'persoontab', 'vektistab']
    
    for script in scripts:
        # run_script(script)
        # import script name as module
        script_module = __import__(script)

if __name__ == "__main__":
    main()
import sys
import yaml
import subprocess
import os
import time

def main(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    run_script = os.path.join(os.path.dirname(__file__), "run.py")

    for model_name in config["models"]:
        print(f"Launching {model_name}", flush=True)

        start = time.time()

        try:
            subprocess.run([
                sys.executable,
                run_script,
                config_path,
                "--model",
                model_name
            ], check=True)

            print(f"Finished {model_name} in {time.time() - start:.1f}s")

        except subprocess.CalledProcessError:
            print(f"\n Failed on model: {model_name}")
            raise


if __name__ == "__main__":
    main(sys.argv[1])
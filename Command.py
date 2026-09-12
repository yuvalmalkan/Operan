import logging
import subprocess
import time
import Constants

class Command:

    @staticmethod
    def execute(command_list: list[str], timeout: int = Constants.DEFAULT_COMMAND_TIMEOUT) -> dict:
        logging.info(f"Executing command: {' '.join(command_list)}")

        try:
            result = subprocess.run(
                command_list,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            is_success = result.returncode == 0
            if not is_success:
                logging.warning(f"Command failed with code {result.returncode}")

            return {
                "success": is_success,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out after {timeout} seconds.")
            
            return {
                "success": False,
                "stdout": "",
                "stderr": "Timeout expired",
                "return_code": -1,
            }

        except FileNotFoundError:
            logging.error(f"Command not found: {command_list[0]}")
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command executable not found",
                "return_code": -2,
            }
        


    @staticmethod
    def open_application(app_name: str) -> bool:
        result = subprocess.run(
            ["open", "-a", app_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            logging.error(f"Failed to open '{app_name}': {result.stderr.strip()}")
            return False

        #applescript check
        deadline = time.time() + Constants.DEFAULT_APP_READY_TIMEOUT
        check_script = f'application "{app_name}" is running'
        

        while time.time() < deadline:
            check_result = subprocess.run(
                ["osascript", "-e", check_script],
                capture_output=True,
                text=True,
                check=False
            )
            
            
            if "true" in check_result.stdout.strip().lower():
                logging.info(f"macOS application '{app_name}' is ready.")
                return True
            
            time.sleep(Constants.DEFAULT_APP_READY_CHECK_INTERVAL)

        logging.error(f"macOS application '{app_name}' did not become ready in time.")
        return False
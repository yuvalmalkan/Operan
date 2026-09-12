import subprocess
import logging
import platform

class Command:

    @staticmethod
    def execute(command_list: list[str], timeout: int = 10) -> dict:
        logging.info(f"Executing command: {' '.join(command_list)}")
        
        try:
            result = subprocess.run(
                command_list,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
            
            is_success = result.returncode == 0
            
            if not is_success:
                logging.warning(f"Command failed with code {result.returncode}")
                
            return {
                "success": is_success,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            logging.error(f"Command timed out after {timeout} seconds.")
            return {"success": False, "stdout": "", "stderr": "Timeout expired", "return_code": -1}
            
        except FileNotFoundError:
            logging.error(f"Command not found: {command_list[0]}")
            return {"success": False, "stdout": "", "stderr": "Command executable not found", "return_code": -2}
            
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {"success": False, "stdout": "", "stderr": str(e), "return_code": -99}

    @staticmethod
    def open_application(app_name: str) -> bool:
        os_name = platform.system()
        command = []
        
        if os_name == "Darwin":
            command = ["open", "-a", app_name]
        elif os_name == "Windows":
            command = ["cmd.exe", "/c", "start", '""', app_name]
        elif os_name == "Linux":
            command = [app_name]
        else:
            logging.error(f"Unsupported OS: {os_name}")
            return False
            
        try:
            # Popen ensures the command runs in the background without blocking the Python script
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info(f"Command sent to open application '{app_name}'.")
            return True
        except Exception as e:
            logging.error(f"Failed to open application '{app_name}': {e}")
            return False
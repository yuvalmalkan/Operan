import subprocess
import logging
import platform
import time
import shutil
import Constants

class Command:
    _LINUX_APP_ALIASES = {
        "Calculator": ("gnome-calculator", "kcalc", "xcalc", "galculator", "mate-calc"),
    }

    @staticmethod
    def execute(command_list: list[str], timeout: int = Constants.DEFAULT_COMMAND_TIMEOUT) -> dict:
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
        ready_process_name = app_name
        
        if os_name == "Darwin":
            command = ["open", "-a", app_name]
        elif os_name == "Windows":
            command = ["cmd.exe", "/c", "start", '""', app_name]
        elif os_name == "Linux":
            linux_candidates = Command._LINUX_APP_ALIASES.get(app_name, (app_name,))
            executable = next((candidate for candidate in linux_candidates if shutil.which(candidate)), None)
            if executable is None:
                logging.error(f"No Linux executable found for '{app_name}'.")
                return False
            command = [executable]
            ready_process_name = executable
        else:
            logging.error(f"Unsupported OS: {os_name}")
            return False
            
        try:
            launcher = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            try:
                launcher_return_code = launcher.wait(timeout=Constants.DEFAULT_LAUNCHER_CHECK_TIMEOUT)
                if launcher_return_code != 0:
                    launcher_error = launcher.stderr.read().strip() if launcher.stderr else ""
                    logging.error(f"Launcher exited with code {launcher_return_code}: {launcher_error}")
                    return False
            except subprocess.TimeoutExpired:
                pass

            if not Command._wait_for_application_ready(ready_process_name, os_name):
                logging.error(f"Application '{app_name}' did not become ready in time.")
                return False

            logging.info(f"Application '{app_name}' is ready.")
            return True
        except Exception as e:
            logging.error(f"Failed to open application '{app_name}': {e}")
            return False

    @staticmethod
    def _wait_for_application_ready(process_name: str, os_name: str) -> bool:
        deadline = time.time() + Constants.DEFAULT_APP_READY_TIMEOUT
        while time.time() < deadline:
            if Command._is_application_running(process_name, os_name):
                return True
            time.sleep(Constants.DEFAULT_APP_READY_CHECK_INTERVAL)
        return False

    @staticmethod
    def _is_application_running(process_name: str, os_name: str) -> bool:
        try:
            if os_name == "Windows":
                result = subprocess.run(
                    ["tasklist"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                return process_name.lower() in result.stdout.lower()

            result = subprocess.run(
                ["pgrep", "-f", process_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
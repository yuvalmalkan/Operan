import subprocess
import logging
import platform

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Command:




    def execute(self, command_list: list[str], timeout: int = 10) -> dict:
        """
        Executes a system command and returns a dictionary with the results.
        
        :param command_list: A list of the command parts (e.g., ["open", "-a", "Calculator"])
        :param timeout: Maximum seconds to wait before the command times out
        :return: A dictionary containing the success status, output (stdout), and errors (stderr)
        """
        logging.info(f"Executing command: {' '.join(command_list)}")
        
        try:
            # Using 'run' executes the command and waits for it to finish
            # capture_output=True captures the returned text (important so the Agent can read it)
            # text=True converts the output from binary to a regular string
            result = subprocess.run(
                command_list,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False # We handle errors ourselves and don't want it to throw an Exception automatically
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
            # Happens if the first command in the list does not exist on the system
            logging.error(f"Command not found: {command_list[0]}")
            return {"success": False, "stdout": "", "stderr": "Command executable not found", "return_code": -2}
            
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {"success": False, "stdout": "", "stderr": str(e), "return_code": -99}





    def open_application(self, app_name: str) -> bool:
        """
        A cross-platform helper function for opening applications.
        """
        os_name = platform.system()
        
        if os_name == "Darwin": # macOS
            result = self.execute(["open", "-a", app_name])
        elif os_name == "Windows":
            # Using cmd to run the 'start' built-in command
            result = self.execute(["cmd.exe", "/c", "start", app_name])
        elif os_name == "Linux":
            result = self.execute([app_name])
        else:
            return False
            
        return result["success"]








if __name__ == "__main__":
    commander = Command()
    current_os = platform.system()
    
    # Example 1: A command that returns text (Dynamic based on OS)
    print("\n--- Example 1: Read System Info ---")
    if current_os == "Darwin":
        info_command = ["sw_vers"]
    elif current_os == "Windows":
        info_command = ["cmd.exe", "/c", "ver"]
    else:
        info_command = ["uname", "-a"]
        
    info_result = commander.execute(info_command)
    if info_result["success"]:
        print(f"System Info:\n{info_result['stdout']}")
        
    # Example 2: A command expected to fail (attempting to run a non-existent command)
    print("\n--- Example 2: Handle Errors ---")
    if current_os == "Windows":
        error_result = commander.execute(["cmd.exe", "/c", "dir", "C:\\folder_that_does_not_exist"])
    else:
        error_result = commander.execute(["ls", "/folder_that_does_not_exist"])
        
    if not error_result["success"]:
        print(f"Caught expected error: {error_result['stderr']}")
        
    # Example 3: Opening applications
    print("\n--- Example 3: Open Applications ---")
    if current_os == "Windows":
        calc_opened = commander.open_application("calc.exe")
    elif current_os == "Darwin":
        calc_opened = commander.open_application("Calculator")
    else:
        calc_opened = commander.open_application("gnome-calculator")
        
    print(f"Calculator opened: {calc_opened}")
    
    # Let's try to open a non-existent application to see how it behaves
    fake_app_opened = commander.open_application("AppThatDoesNotExist123")
    print(f"Fake App opened: {fake_app_opened}")

    print("\n\n\n")
    
    # Example 4: List directory content
    if current_os == "Windows":
        print(commander.execute(['cmd.exe', '/c', 'dir'])['stdout'])
    else:
        print(commander.execute(['ls', '-la'])['stdout'])
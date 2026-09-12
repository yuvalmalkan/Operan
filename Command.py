import logging
import subprocess
import time

import Constants


class Command:
    @staticmethod
    def execute(
        command_list: list[str],
        timeout: int = Constants.DEFAULT_COMMAND_TIMEOUT,
    ) -> dict:
        logging.info("Executing command: %s", " ".join(command_list))

        try:
            result = subprocess.run(
                command_list,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            logging.error("Command timed out after %s seconds.", timeout)
            return {
                "success": False,
                "stdout": "",
                "stderr": "Timeout expired",
                "return_code": -1,
            }
        except FileNotFoundError:
            logging.error("Command not found: %s", command_list[0])
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command executable not found",
                "return_code": -2,
            }

        is_success = result.returncode == 0
        if not is_success:
            logging.warning("Command failed with code %s", result.returncode)

        return {
            "success": is_success,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "return_code": result.returncode,
        }

    @staticmethod
    def open_application(app_name: str) -> bool:
        try:
            launcher = subprocess.Popen(
                ["open", "-a", app_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                launcher_return_code = launcher.wait(
                    timeout=Constants.DEFAULT_LAUNCHER_CHECK_TIMEOUT
                )
                if launcher_return_code != 0:
                    launcher_error = (
                        launcher.stderr.read().strip() if launcher.stderr else ""
                    )
                    logging.error(
                        "macOS application launcher exited with code %s: %s",
                        launcher_return_code,
                        launcher_error,
                    )
                    return False
            except subprocess.TimeoutExpired:
                pass

            if not Command._wait_for_application_ready(app_name):
                logging.error(
                    "macOS application '%s' did not become ready in time.",
                    app_name,
                )
                return False

            logging.info("macOS application '%s' is ready.", app_name)
            return True
        except OSError as error:
            logging.error("Failed to open macOS application '%s': %s", app_name, error)
            return False

    @staticmethod
    def _wait_for_application_ready(process_name: str) -> bool:
        deadline = time.time() + Constants.DEFAULT_APP_READY_TIMEOUT
        while time.time() < deadline:
            if Command._is_application_running(process_name):
                return True
            time.sleep(Constants.DEFAULT_APP_READY_CHECK_INTERVAL)
        return False

    @staticmethod
    def _is_application_running(process_name: str) -> bool:
        result = subprocess.run(
            ["pgrep", "-f", process_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0

import subprocess

class HealthCheck:
    def __init__(self, commands):
        self.commands = commands

    def execute_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    def generate_report(self):
        report = ""
        for title, cmd_info in self.commands.items():
            cmd = cmd_info['command']
            desc = cmd_info['description']
            output = self.execute_command(cmd)
            report += f"## {title}\n"
            report += f"## {desc}\n\n"
            report += f"{output}\n\n"
        return report

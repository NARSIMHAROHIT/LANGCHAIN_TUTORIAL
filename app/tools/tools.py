
@tool
def plan_linux_command(query: str) -> str:
    """
    Analyze the user's request and suggest the most appropriate Linux command(s)
    based on official Linux documentation and best practices.
    """
    response = "identified command from Linux documentation"
    return (
        f"Planned command for query '{query}': {response}. "
        "This command is selected based on standard Linux documentation."
    )


@tool
def inspect_system(query: str) -> str:
    """
    Inspect system state using read-only Linux commands.
    No system changes are performed.
    """
    response = "read-only inspection command from documentation"
    return (
        f"Inspection suggestion for '{query}': {response}. "
        "This command is safe and does not modify the system."
    )


@tool
def explain_linux_command(command: str) -> str:
    """
    Explain what a Linux command does using documented behavior and flags.
    """
    response = "documented explanation of command and flags"
    return (
        f"Explanation for command '{command}': {response}. "
        "Explanation is based on official man pages."
    )


@tool
def execute_linux_command(command: str) -> str:
    """
    Execute the approved Linux command and return its output.
    This tool should only be used after planning and explanation.
    """
    response = "command executed successfully (simulated output)"
    return (
        f"Execution result for command '{command}': {response}."
    )


@tool
def verify_command_result(command: str) -> str:
    """
    Verify the result of a previously executed command using documented
    verification techniques.
    """
    response = "verification command from documentation"
    return (
        f"Verification for '{command}': {response}. "
        "This confirms whether the action was successful."
    )


@tool
def search_alternative_linux_commands(command: str) -> str:
    """
    Search for alternative or modern Linux commands that provide similar
    functionality based on current best practices.
    """
    response = "modern or recommended alternative command"
    return (
        f"Alternative commands for '{command}': {response}. "
        "Suggested based on modern Linux best practices."
    )


@tool
def compare_linux_commands(command_a: str, command_b: str) -> str:
    """
    Compare two Linux commands based on their documented purpose,
    differences, and recommended usage.
    """
    response = "documented comparison and recommendation"
    return (
        f"Comparison between '{command_a}' and '{command_b}': {response}. "
        "Comparison is based on official documentation and usage guidelines."
    )


@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

import typer
from adapters.google_adapter import authenticate, get_service, fetch_emails, import_emails
from handlers.rule_handler import rule_handler
from schema.migrate import run_migrations
import subprocess
app = typer.Typer()


@app.command()
def run_tests():
    """
    Runs pytest tests.
    """
    typer.echo("Running pytest tests...")
    try:
        subprocess.run(["pytest", "tests/"], check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error running tests: {e}")
    else:
        typer.echo("Tests completed successfully.")


def authenticate_with_google():
    """
    Authenticates with Google and returns the Gmail service.
    """
    credentials = authenticate()
    service = get_service('gmail', 'v1', credentials=credentials)
    return service


@app.command()
def import_emails_from_inbox():
    """
    Imports emails from the gmail inbox using Oauth2.
    """
    service = authenticate_with_google()
    messages = fetch_emails(service)
    import_emails(messages, service)


@app.command()
def execute_rule():
    """
    Executes a rules on the emails such as mark_as_read/unread/move_to_inbox.
    """
    service = authenticate_with_google()
    rule_handler(service)


def main():
    print("******************************* Gmail CLI **************************************")
    print("---------- For importing emails from inbox and performing operations ----------")
    print("-------------------------------------------------------------------------------\n\n")
    run_migrations()
    app()


if __name__ == "__main__":
    main()

from adapters.google_adapter import authenticate, get_service, fetch_emails, import_emails
from handlers.rule_handler import rule_handler
from schema.migrate import run_migrations


def authenticate_with_google():
    credentials = authenticate()
    service = get_service('gmail', 'v1', credentials=credentials)
    return service


def import_emails_from_inbox(service):
    messages = fetch_emails(service)
    import_emails(messages, service)


def execute_rule(service):
    rule_handler(service)


def main():
    print("******************************* Gmail CLI **************************************")
    print("---------- For importing emails from inbox and performing operations ----------")
    print("-------------------------------------------------------------------------------\n\n")
    run_migrations()
    service = authenticate_with_google()
    while True:
        print("\nOptions:")
        print("1. Import emails from inbox")
        print("2. Execute rule")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            import_emails_from_inbox(service)
        elif choice == '2':
            execute_rule(service)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()

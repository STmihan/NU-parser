from datetime import datetime
import run as Run


def main():
    time = datetime.now()
    Run.save_all(pretty=True, forceUpdate=True)
    print("Done in " + str(datetime.now() - time))


if __name__ == "__main__":
    main()

from .extracters import References


def main():
    for reference in References.load("references.yaml").messages():
        print(reference)


if __name__ == "__main__":
    main()

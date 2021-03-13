from .extracters import references


def main():
    for reference in references.load("references.yaml").messages():
        print(reference)


if __name__ == "__main__":
    main()


INPUT_FILE = "transactions.txt"
OUTPUT_FILE = "report.txt"


def read_transactions(filename):
    totals = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                name, amount = line.strip().split(",")
                amount = float(amount)
                totals[name] = totals.get(name, 0) + amount

    except FileNotFoundError:
        print("File not found.")
        return {}

    return totals


def print_summary(totals):
    sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)

    for name, total in sorted_totals:
        print(f"{name}: {total:.2f}")


def write_report(totals, filename):
    sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)

    with open(filename, "w") as file:
        for name, total in sorted_totals:
            file.write(f"{name}: {total:.2f}\n")


def main():
    totals = read_transactions(INPUT_FILE)
    print_summary(totals)
    write_report(totals, OUTPUT_FILE)


if __name__ == "__main__":
    main()

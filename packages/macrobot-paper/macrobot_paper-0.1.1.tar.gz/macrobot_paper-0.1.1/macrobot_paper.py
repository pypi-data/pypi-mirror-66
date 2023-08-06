import argparse

def main():
    print("It's alive!")

    parser = argparse.ArgumentParser(description='Macrobot analysis software.')
    parser.add_argument('-s', '--source_path', required=True,
                        help='Directory containing images to segment.')
    parser.add_argument('-d', '--destination_path', required=True,
                        help='Directory to store the result images.')
    parser.add_argument('-p', '--procedure', required=True,
                        help='Pathogen, choose bgt or rust.')

    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
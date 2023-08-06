from b3tojson import processor, fetcher

import argparse

def process_args():
    parser = argparse.ArgumentParser(description='B3 to JSON format converter')
    parser.add_argument('--fetch', dest='should_fetch', action='store_true', help='Specifies if data file should be fetched from server')
    parser.add_argument('--b3_file', dest='b3_file', action='store', help='Local B3 data file path')
    parser.add_argument('--json_file', dest='json_file', action='store', help='Target JSON file path', default=fetcher.JSON_FILE)

    args = parser.parse_args()
    if args.should_fetch and args.b3_file is not None:
        print("Ambiguous flags --fetch and --b3_file. Quitting")

    return(args)
   
def main():
    args = process_args()

    if args.should_fetch:
        b3_file = fetcher.get_b3_data()
    else:
        b3_file = args.b3_file

    obj = processor.FileHandle(b3_file, args.json_file)
    obj.analyze_file()
    obj.save_json()
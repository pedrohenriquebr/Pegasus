import argparse
from pegasus import Pegasus

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processar arquivo csv do Banco Inter')
    parser.add_argument('--filename', type=str, default=None, required=False)
    args = parser.parse_args()
    pegasus  = Pegasus(debug=True)
    if args.filename:
        pegasus.append_dataframe(args.filename)
    pegasus.load_spreadsheet()
    pegasus.load_dataframe()
    pegasus.transform()
    pegasus.export_csv()
    pegasus.export_xlsx()
from b3tojson.data import Company, Stock

import jsonpickle


class FileHandle():
    companies: {Company}

    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        self.companies = {}

    def _process_raw_data(self, lines):
        lines = [line.strip() for line in lines]
        for line in lines:
            # HEADER -- just skipping it
            if line.startswith('00'):
                continue
            # COMPANY DATA
            elif line.startswith('01'):
                code = line[2:6]
                self.companies[code] = Company(code, line[6:66], line[66:78])
            # STOCK DATA
            elif line.startswith('02'):
                code = line[14:18]
                bdi = line[18:21]
                # 002: STD STOCK // 012: FII
                if bdi == '002' or bdi == '012':
                    self.companies[code].add_stock(Stock(line[2:14], bdi,
                                                         line[21:81],
                                                         line[133:143]))

    def _to_json(self):
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        return jsonpickle.encode(self.companies, unpicklable=False)

    def analyze_file(self):
        try:
            with open(self.in_file, "r", encoding="utf-8") as fd:
                lines = fd.readlines()
        except FileNotFoundError:
            print(f"Could not open file {self.in_file}")
        # TODO: Handle file enconding by iteself
        except UnicodeDecodeError:
            print("Please, ensure the file to be encoded as UTF-8")
        except Exception:
            raise
        else:
            self._process_raw_data(lines)

    def save_json(self):
        encoded = self._to_json()

        with open(self.out_file, 'w', encoding="utf-8") as fd:
            fd.write(encoded)

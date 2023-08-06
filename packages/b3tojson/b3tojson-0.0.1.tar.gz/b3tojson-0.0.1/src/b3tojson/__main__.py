from b3tojson import processor

obj = processor.FileHandle("../TITULOS_NEGOCIAVEIS.TXT", '../stocks_data.json')
obj.analyze_file()
obj.save_json()
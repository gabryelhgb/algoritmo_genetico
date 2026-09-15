import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from algoritmo_genetico import executar_algoritmo_genetico


class ServidorAlgoritmo(BaseHTTPRequestHandler):
    def adicionar_cabecalhos(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "http://localhost:3000")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self.adicionar_cabecalhos()

    def do_POST(self):
        if self.path != "/executar":
            self.adicionar_cabecalhos(404)
            self.wfile.write(json.dumps({"erro": "Rota não encontrada"}).encode("utf-8"))
            return

        try:
            resultado = executar_algoritmo_genetico()
            resposta = json.dumps(resultado, ensure_ascii=False).encode("utf-8")
            self.adicionar_cabecalhos()
            self.wfile.write(resposta)
        except Exception as erro:
            self.adicionar_cabecalhos(500)
            resposta = json.dumps({"erro": str(erro)}, ensure_ascii=False).encode("utf-8")
            self.wfile.write(resposta)

    def log_message(self, formato, *argumentos):
        return


if __name__ == "__main__":
    endereco = ("localhost", 8000)
    servidor = ThreadingHTTPServer(endereco, ServidorAlgoritmo)
    print("Backend disponível em http://localhost:8000")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()
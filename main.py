from flask import Flask, jsonify, render_template_string
import psutil

app = Flask(__name__)
fila_ultimos_registros = []


@app.route('/')
def home():
    return render_template_string('''
<html>
    <head>
        <title>Monitoramento de Recursos</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            $(document).ready(function(){
                setInterval(function(){
                    $.getJSON('/status', function(data) {
                        $('#cpu_usage').text(data.cpu);
                        $('#ram_usage').text(data.ram);
                    });
                }, 1000); // Atualiza a cada 1 segundo
            });
        </script>
    </head>
    <body>
        <h1>Monitoramento de Recursos do Sistema</h1>
        <p>CPU: <span id="cpu_usage">Carregando...</span>%</p>
        <p>RAM: <span id="ram_usage">Carregando...</span>%</p>
    </body>
</html>
''')

@app.route('/status')
def status():
    #uso total de cpu
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    fila_ultimos_registros.append({"cpu": cpu_usage,"ram": ram_usage})
    if len(fila_ultimos_registros) > 5:
        fila_ultimos_registros.pop(0)
    print(fila_ultimos_registros)
    return jsonify(cpu=cpu_usage, ram=ram_usage)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
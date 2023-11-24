from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from Connection import Connection as conn
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

with open('sleep_quality_model.pickle', 'rb') as f:
    sleep_quality_model = pickle.load(f)

with open('stress_model.pickle', 'rb') as f:
    stress_model = pickle.load(f)


@app.route("/qualificar")
def qualificar_sono_estresse():
    idade = int(request.args.get('idade'))
    duracao_sono = int(request.args.get('duracao_sono'))
    tempo_atividade_fisica = int(request.args.get('tempo_atividade_fisica'))

    entrada_sleep_quality = np.array(
        [[idade, duracao_sono, tempo_atividade_fisica]])

    qualidade_sono = sleep_quality_model.predict(entrada_sleep_quality)

    entrada_stress_model = np.array(
        [[idade, duracao_sono, qualidade_sono.tolist()[0], tempo_atividade_fisica]])

    nivel_estresse = stress_model.predict(entrada_stress_model)

    return jsonify({'qualidade_sono': qualidade_sono.tolist()[0], 'nivel_estresse': nivel_estresse.tolist()[0]})


@app.route("/cadastro", methods=["POST"])
def insert_cliente() -> jsonify:
    try:
        cliente_data = request.get_json()
        conn.inserir_cliente(cliente_data)
        return jsonify(cliente_data), 201
    except Exception as e:
        print("Erro ao inserir novo cliente: ", e)
        return jsonify({"message": "An error occurred."}), 500


@app.route("/bmi", methods=["PUT"])
def put_bmi_cliente() -> jsonify:
    try:
        cliente_data = request.get_json()
        print(cliente_data)
        conn.alterar_cliente(cliente_data)
        return jsonify(cliente_data), 201
    except Exception as e:
        print("Erro ao inserir bmi do cliente: ", e)
        return jsonify({"message": "An error occurred."}), 500


@app.route("/validar")
def get_client_by_user():
    user = request.args.get('usuario')
    password = request.args.get('senha')
    try:
        stored_password = conn.buscar_cliente_by_user(user)
        # Use a secure password comparison method here
        if password == stored_password:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Invalid password"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {e}"})


@app.route("/user/<user>")
def get_id_cliente_data_cliente_by_user(user):
    try:
        user = conn.get_id_cliente_by_user(user)
        return jsonify({"id_cliente": user["id"], "data_nasc": user["data"]}), 200
    except Exception as e:
        print("Erro ao buscar id do cliente: ", e)
        return jsonify({"message": "An error occurred."}), 500


@app.route("/sono", methods=["POST"])
def insert_sono() -> jsonify:
    try:
        sono_data = request.get_json()
        conn.inserir_sono_cliente(sono_data)
        return jsonify(sono_data), 201
    except Exception as e:
        print("Erro ao inserir sono do cliente: ", e)
        return jsonify({"message": "An error occurred."}), 500


@app.route("/sonos/<idCliente>")
def select_sonos_by_id_cliente(idCliente):
    try:
        sonos = conn.find_all_sono_by_id_cliente(idCliente)
        return jsonify({"sonos": sonos}), 200
    except Exception as e:
        print("Erro ao inserir sono do cliente: ", e)
        return jsonify({"message": "An error occurred."}), 500


@app.route("/sonos/<idSono>", methods=["DELETE"])
def delete_sono_by_id(idSono):
    try:
        if (conn.excluir_sono_cliente(idSono)):
            return jsonify({"delete": True}), 200
        else:
            return jsonify({"delete": False}), 400
    except Exception as e:
        print("Erro ao inserir sono do cliente: ", e)
        return jsonify({"message": "An error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8080)

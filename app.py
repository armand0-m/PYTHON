from flask import Flask, render_template, make_response, jsonify, request

app=Flask(__name__)

PORT=3200
HOST='0.0.0.0'

INFO={
    "languages":{
        "es":"Spanish",
        "en":"English",
        "fr":"French",
    },
    "colors":{
        "r":"Red",
        "g":"Green",
        "b":"Blue",
    },
    "clouds":{
        "IBM":"IBM CLOUD",
        "AMAZON":"AWS",
        "MICROSOFT":"AZURE",
    }
}
#GET METOD
#principal de prueba
@app.route("/")
def home():
    return"<h1 style='color_blue'>This is HOME!</h1>"
#MUESTRA LA INFORMACION DEL ARCHIVO DE LA RUTA
@app.route("/temp")
def template():
    return render_template('index.html')
#SE ENVIA DATOS DE QUERY
@app.route("/qstr")
def query_string():
    if request.args:
        req=request.args
        res={}
        for key, value in req.items():
            res[key]=value
        res=make_response(jsonify(res),200)
        return res
    res=make_response(jsonify({"Error":"No query strings"}),400)
    return res
#MUESTRA TODOS LOS DATOS DEL ARCHIVO JSON : INFO
@app.route("/json")
def get_json():
    res=make_response(jsonify(INFO),200)
    return res
#
@app.route("/json/<collection>/<member>")
def get_data(collection,member):
    if collection in INFO:
        member=INFO[collection].get(member)
        if member:
            res=make_response(jsonify({"res":member}),200)
            return res
        res=make_response(jsonify({"error":"MEMBER Not found"}),400)
        return res 
    res=make_response(jsonify({"error":"COLLECTION Not found"}),400)
    return res

#POST METHOD : AGREGAR
@app.route("/json/<collection>", methods=["POST"])
def create_collection(collection):
    req=request.get_json()
    if collection in INFO:
        res=make_response(jsonify({"error":"Collection already exists"}),400)
        return res
    INFO.update({collection:req})

    res=make_response(jsonify({"message":"Collection created succesfully"}),200)    
    return res
#PUT METHOD : EDITAR
@app.route("/json/<collection>/<member>", methods=["PUT"])
def update_collection(collection,member):
    req=request.get_json()
    if collection in INFO:
        if member:
            INFO[collection][member] = req["new"]
            res=make_response(jsonify({"res":INFO[collection]}),400)
            return res

        res=make_response(jsonify({"error":"MEMBER not found"}),200)    
        return res 
    res=make_response(jsonify({"error":"COLLECTION not found"}),200)    
    return res 
#DELETE METHOD ELIMINAR
@app.route("/json/<collection>",methods=["DELETE"])
def delete_collection(collection):
    if collection in INFO:
        del INFO[collection]
        res=make_response(jsonify(INFO),200)
        return res
    res=make_response(jsonify({"error":"collection not found"}),200)
    return res

if __name__=="__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)


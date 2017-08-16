from flask import Flask,render_template,request
import boto3

client = boto3.client('s3')
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("Main.html")

@app.route('/bucket_list',methods=['POST'])
def bucket_list():
    buckets = client.list_buckets()
    buck_list = []
    for i in buckets['Buckets']:
        buck_list.append((i['Name'],str(i['CreationDate'])))

    return render_template("BucketList.html",buck_list=buck_list)

@app.route('/get_objects',methods=['POST'])
def get_objects():
    objects = client.list_objects_v2(Bucket=list(request.form)[0])
    obj_list = []
    try:
        for i in objects['Contents']:
            obj_list.append((i['Key'],i['LastModified'],i['Size'],i['StorageClass']))

        return render_template("ObjectList.html",obj_list=obj_list)

    except:
        return "No data"

if __name__ == '__main__':
    app.run()

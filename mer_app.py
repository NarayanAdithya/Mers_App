from app import app,db
from app.models import User,ticket,train,requests_


@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'train':train,'ticket':ticket,'requests':requests_}



if __name__=="__main__":
    app.run(debug=True)
from odoorpc import ODOO

class LibraryAPI():
    def __init__(self,srv,port,db,user,pwd,modelname):
        self.api = ODOO(srv,port=port)
        self.api.login(db,user,pwd)
        self.uid = self.api.env.uid
        self.model =modelname
        self.Model = self.api.env[self.model]

    def execute(self,method,arg_list,kwarg_dict=None):
        return self.api.execute(
                self.model,method,*arg_list,**kwarg_dict)

    def search_read(self,text=None):
        domain = [('name','ilike',text)] if text else []
        fields = ['id','name','user_type']
        return self.Model.search_read(domain,fields)

    def create(self,title):
        vals = {'name':title}
        return self.Model.create(vals)

    def write(self,title,id):
        vals = {'name':title}
        self.Model.write(id,vals)

    def unlink(self,id):
        return self.Model.unlink(id)

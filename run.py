from app import app, db
from app.models import Company, Employee, Record 

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Company': Company, 'Employee': Employee, 'Record': Record}

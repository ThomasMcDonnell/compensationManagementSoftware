from app import create_app, db
from app.models import Company, Employee, Record 

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Company': Company, 'Employee': Employee, 'Record': Record}

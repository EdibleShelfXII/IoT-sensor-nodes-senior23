from django.core.management import call_command

def update_db_from_api(): 
    call_command('runjobs quarter_hourly')
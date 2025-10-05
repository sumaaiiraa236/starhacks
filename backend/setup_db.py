from db import init_db, upsert_elder_profile
init_db()
upsert_elder_profile('e1','John Doe', {'hr_max':110,'spo2_min':93.0,'bp_sys_max':160}, {'primary_family':'Jane Doe','ems_number':'911'})
print('✅ SQLite DB initialized at backend/carecrew.db')

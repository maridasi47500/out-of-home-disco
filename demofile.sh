
mkdir templates 
python3 scaffold.py logement title description
python3 scaffold.py logementhasuser  user_id logement_id
python3 scaffold.py user username password email phone country_id:references musicstyle_id:references
python3 scaffold.py country name
python3 scaffold.py userhasjob user_id job_id logement_id
python3 scaffold.py job name
python3 scaffold.py musicstyle name
python3 scaffold.py pianoaccompaniedpiece musicalinstrument_id:references title composer musicstyle_id:references
python3 scaffold.py musicalinstrument name

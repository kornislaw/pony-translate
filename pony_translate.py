from __future__ import absolute_import, print_function

from datetime import datetime
from pony.orm import *

from datetime import datetime


db = Database()


class Translation(db.Entity):
    _table_ = 'GOOGLE_TRANSLATIONS'
    id = PrimaryKey(int, auto=True)
    source_lang_code = Optional(str)  # 2-chars
    target_lang_code = Required(str, default='en')  # 2-chars
    input = Required(str)
    output = Required(str)
    created_at = Required(datetime)
    updated_at = Optional(datetime)


db.bind("sqlite", ":memory:")
db.generate_mapping(create_tables=True)

@db_session
def populate_database():
    t1 = Translation(source_lang_code='PL', target_lang_code='EN', input='krzesło', output='chair', created_at=datetime.now())
    set_translation('PL', 'EN', 'noga', 'leg')


@db_session
def get_translations(source, target, input):
    return select(t for t in Translation if t.source_lang_code == source and t.target_lang_code == target and t.input == input)[:]


@db_session
def set_translation(source, target, input, output):
    ts = get_translations(source=source, target=target, input=input)[:]
    if len(ts) > 0:
        t = ts[0]
        t.output = output
        t.updated_at = datetime.now()
    else:
        t = Translation(source_lang_code=source, target_lang_code=target, 
        input=input, output=output, created_at=datetime.now())
    commit()

populate_database()

with db_session():

    ts = get_translations('PL', 'EN', 'krzesło')
    ts.show()
    print()

    ts = get_translations('PL', 'EN', 'noga')
    ts.show()
    print()

    set_translation('PL', 'EN', 'noga', 'leggg')
    ts = select(t for t in Translation)

    ts.show()

    for t in ts:
        print(t.input, t.output)

import datetime

from flask import request
from flask.views import MethodView

from app import db, app
from app.models import Readers


class ReaderApi(MethodView):
    def get(self, reader_id):
        if not reader_id:
            # Readers是数据库表名，readerslist是查出的列表
            readerslist: [Readers] = Readers.query.all()
            results = [
                {
                    'id': readers.reader_id,
                    'name': readers.reader_name,
                    'password': readers.reader_password,
                    'registration_date': readers.registration_date,
                    'reader_type': readers.reader_type,
                    'is_active': readers.is_active,
                    'account_balance': readers.account_balance
                } for readers in readerslist
            ]
            return {
                'status': 'success',
                'message': '读者数据查询成功',
                'results': results
            }
        single: Readers = Readers.query.get(reader_id)
        return {
            'status': 'success',
            'message': '读者数据查询成功',
            'results': {
                'id': single.reader_id,
                'name': single.reader_name,
                'password': single.reader_password,
                'registration_date': single.registration_date,
                'reader_type': single.reader_type,
                'is_active': single.is_active,
                'account_balance': single.account_balance
            }
        }

    def post(self):
        form = request.json
        newreader = Readers()
        newreader.reader_name = form.get('reader_name')
        newreader.reader_password = form.get('reader_password')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        newreader.registration_date = now_time
        newreader.reader_type = form.get('reader_type')
        db.session.add(newreader)
        db.session.commit()

        return {
            'status': 'success',
            'message': '数据添加成功'
        }


reader_view = ReaderApi.as_view('reader_api')
app.add_url_rule('/readers/', defaults={'reader_id': None}, view_func=reader_view, methods=['GET'])
app.add_url_rule('/readers/', view_func=reader_view, methods=['POST'])
app.add_url_rule('/readers/<int:reader_id>', view_func=reader_view, methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/api/books', methods=['GET', 'POST'])

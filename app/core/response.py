from flask import jsonify

class Result:
    @staticmethod
    def success(data=None, message='success'):
        return jsonify({
            'code': 0,
            'message': message,
            'data': data
        })

import random

import flask
from flask import jsonify

from data import db_session

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/generate_palettes/<int:quantity>', methods=['GET'])
def generate_palettes(quantity):
    colors_letters = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}
    palettes = []
    for _ in range(quantity):
        colors = []
        for _ in range(5):
            color = ''
            for _ in range(6):
                num_let = str(random.randint(0, 15))
                if num_let in colors_letters.keys():
                    num_let = colors_letters[num_let]
                color += num_let
            colors.append('#' + color)
        palettes.append(colors)
    if not palettes:
        return jsonify(
            {
                'error': 'error'
            }
        )
    return jsonify(
        {
            'random_palettes': palettes
        })



